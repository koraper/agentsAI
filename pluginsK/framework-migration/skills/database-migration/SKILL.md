---
name: database-migration
description: Execute 데이터베이스 migrations 전반에 걸쳐 ORMs 및 플랫폼 와 함께 zero-downtime strategies, 데이터 변환, 및 롤백 절차. Use 때 migrating databases, changing 스키마, performing 데이터 transformations, 또는 implementing zero-downtime 배포 strategies.
---

# 데이터베이스 마이그레이션

마스터 데이터베이스 스키마 및 데이터 migrations 전반에 걸쳐 ORMs (Sequelize, TypeORM, Prisma), 포함하여 롤백 strategies 및 zero-downtime deployments.

## 때 에 Use This Skill

- Migrating 사이 다른 ORMs
- Performing 스키마 transformations
- Moving 데이터 사이 databases
- Implementing 롤백 절차
- Zero-downtime deployments
- 데이터베이스 버전 업그레이드합니다
- 데이터 모델 리팩토링

## ORM Migrations

### Sequelize Migrations
```javascript
// migrations/20231201-create-users.js
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.createTable('users', {
      id: {
        type: Sequelize.INTEGER,
        primaryKey: true,
        autoIncrement: true
      },
      email: {
        type: Sequelize.STRING,
        unique: true,
        allowNull: false
      },
      createdAt: Sequelize.DATE,
      updatedAt: Sequelize.DATE
    });
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.dropTable('users');
  }
};

// Run: npx sequelize-cli db:migrate
// Rollback: npx sequelize-cli db:migrate:undo
```

### TypeORM Migrations
```typescript
// migrations/1701234567-CreateUsers.ts
import { MigrationInterface, QueryRunner, Table } from 'typeorm';

export class CreateUsers1701234567 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.createTable(
      new Table({
        name: 'users',
        columns: [
          {
            name: 'id',
            type: 'int',
            isPrimary: true,
            isGenerated: true,
            generationStrategy: 'increment'
          },
          {
            name: 'email',
            type: 'varchar',
            isUnique: true
          },
          {
            name: 'created_at',
            type: 'timestamp',
            default: 'CURRENT_TIMESTAMP'
          }
        ]
      })
    );
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.dropTable('users');
  }
}

// Run: npm run typeorm migration:run
// Rollback: npm run typeorm migration:revert
```

### Prisma Migrations
```prisma
// schema.prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  createdAt DateTime @default(now())
}

// Generate migration: npx prisma migrate dev --name create_users
// Apply: npx prisma migrate deploy
```

## 스키마 Transformations

### Adding 열 와 함께 Defaults
```javascript
// Safe migration: add column with default
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.addColumn('users', 'status', {
      type: Sequelize.STRING,
      defaultValue: 'active',
      allowNull: false
    });
  },

  down: async (queryInterface) => {
    await queryInterface.removeColumn('users', 'status');
  }
};
```

### Renaming 열 (Zero Downtime)
```javascript
// Step 1: Add new column
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.addColumn('users', 'full_name', {
      type: Sequelize.STRING
    });

    // Copy data from old column
    await queryInterface.sequelize.query(
      'UPDATE users SET full_name = name'
    );
  },

  down: async (queryInterface) => {
    await queryInterface.removeColumn('users', 'full_name');
  }
};

// Step 2: Update application to use new column

// Step 3: Remove old column
module.exports = {
  up: async (queryInterface) => {
    await queryInterface.removeColumn('users', 'name');
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.addColumn('users', 'name', {
      type: Sequelize.STRING
    });
  }
};
```

### Changing 열 유형
```javascript
module.exports = {
  up: async (queryInterface, Sequelize) => {
    // For large tables, use multi-step approach

    // 1. Add new column
    await queryInterface.addColumn('users', 'age_new', {
      type: Sequelize.INTEGER
    });

    // 2. Copy and transform data
    await queryInterface.sequelize.query(`
      UPDATE users
      SET age_new = CAST(age AS INTEGER)
      WHERE age IS NOT NULL
    `);

    // 3. Drop old column
    await queryInterface.removeColumn('users', 'age');

    // 4. Rename new column
    await queryInterface.renameColumn('users', 'age_new', 'age');
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.changeColumn('users', 'age', {
      type: Sequelize.STRING
    });
  }
};
```

## 데이터 Transformations

### 복잡한 데이터 마이그레이션
```javascript
module.exports = {
  up: async (queryInterface, Sequelize) => {
    // Get all records
    const [users] = await queryInterface.sequelize.query(
      'SELECT id, address_string FROM users'
    );

    // Transform each record
    for (const user of users) {
      const addressParts = user.address_string.split(',');

      await queryInterface.sequelize.query(
        `UPDATE users
         SET street = :street,
             city = :city,
             state = :state
         WHERE id = :id`,
        {
          replacements: {
            id: user.id,
            street: addressParts[0]?.trim(),
            city: addressParts[1]?.trim(),
            state: addressParts[2]?.trim()
          }
        }
      );
    }

    // Drop old column
    await queryInterface.removeColumn('users', 'address_string');
  },

  down: async (queryInterface, Sequelize) => {
    // Reconstruct original column
    await queryInterface.addColumn('users', 'address_string', {
      type: Sequelize.STRING
    });

    await queryInterface.sequelize.query(`
      UPDATE users
      SET address_string = CONCAT(street, ', ', city, ', ', state)
    `);

    await queryInterface.removeColumn('users', 'street');
    await queryInterface.removeColumn('users', 'city');
    await queryInterface.removeColumn('users', 'state');
  }
};
```

## 롤백 Strategies

### 트랜잭션-Based Migrations
```javascript
module.exports = {
  up: async (queryInterface, Sequelize) => {
    const transaction = await queryInterface.sequelize.transaction();

    try {
      await queryInterface.addColumn(
        'users',
        'verified',
        { type: Sequelize.BOOLEAN, defaultValue: false },
        { transaction }
      );

      await queryInterface.sequelize.query(
        'UPDATE users SET verified = true WHERE email_verified_at IS NOT NULL',
        { transaction }
      );

      await transaction.commit();
    } catch (error) {
      await transaction.rollback();
      throw error;
    }
  },

  down: async (queryInterface) => {
    await queryInterface.removeColumn('users', 'verified');
  }
};
```

### Checkpoint-Based 롤백
```javascript
module.exports = {
  up: async (queryInterface, Sequelize) => {
    // Create backup table
    await queryInterface.sequelize.query(
      'CREATE TABLE users_backup AS SELECT * FROM users'
    );

    try {
      // Perform migration
      await queryInterface.addColumn('users', 'new_field', {
        type: Sequelize.STRING
      });

      // Verify migration
      const [result] = await queryInterface.sequelize.query(
        "SELECT COUNT(*) as count FROM users WHERE new_field IS NULL"
      );

      if (result[0].count > 0) {
        throw new Error('Migration verification failed');
      }

      // Drop backup
      await queryInterface.dropTable('users_backup');
    } catch (error) {
      // Restore from backup
      await queryInterface.sequelize.query('DROP TABLE users');
      await queryInterface.sequelize.query(
        'CREATE TABLE users AS SELECT * FROM users_backup'
      );
      await queryInterface.dropTable('users_backup');
      throw error;
    }
  }
};
```

## Zero-Downtime Migrations

### Blue-Green 배포 전략
```javascript
// Phase 1: Make changes backward compatible
module.exports = {
  up: async (queryInterface, Sequelize) => {
    // Add new column (both old and new code can work)
    await queryInterface.addColumn('users', 'email_new', {
      type: Sequelize.STRING
    });
  }
};

// Phase 2: Deploy code that writes to both columns

// Phase 3: Backfill data
module.exports = {
  up: async (queryInterface) => {
    await queryInterface.sequelize.query(`
      UPDATE users
      SET email_new = email
      WHERE email_new IS NULL
    `);
  }
};

// Phase 4: Deploy code that reads from new column

// Phase 5: Remove old column
module.exports = {
  up: async (queryInterface) => {
    await queryInterface.removeColumn('users', 'email');
  }
};
```

## Cross-데이터베이스 Migrations

### PostgreSQL 에 MySQL
```javascript
// Handle differences
module.exports = {
  up: async (queryInterface, Sequelize) => {
    const dialectName = queryInterface.sequelize.getDialect();

    if (dialectName === 'mysql') {
      await queryInterface.createTable('users', {
        id: {
          type: Sequelize.INTEGER,
          primaryKey: true,
          autoIncrement: true
        },
        data: {
          type: Sequelize.JSON  // MySQL JSON type
        }
      });
    } else if (dialectName === 'postgres') {
      await queryInterface.createTable('users', {
        id: {
          type: Sequelize.INTEGER,
          primaryKey: true,
          autoIncrement: true
        },
        data: {
          type: Sequelize.JSONB  // PostgreSQL JSONB type
        }
      });
    }
  }
};
```

## 리소스

- **참조/orm-switching.md**: ORM 마이그레이션 안내합니다
- **참조/스키마-마이그레이션.md**: 스키마 변환 패턴
- **참조/데이터-변환.md**: 데이터 마이그레이션 스크립트
- **참조/롤백-strategies.md**: 롤백 절차
- **자산/스키마-마이그레이션-템플릿.sql**: SQL 마이그레이션 템플릿
- **자산/데이터-마이그레이션-스크립트.py**: 데이터 마이그레이션 utilities
- **스크립트/test-마이그레이션.sh**: 마이그레이션 테스트 스크립트

## 최선의 관행

1. **항상 Provide 롤백**: 모든 up() needs a down()
2. **Test Migrations**: Test 에 staging 첫 번째
3. **Use Transactions**: 원자적 migrations 때 possible
4. **백업 첫 번째**: 항상 백업 이전 마이그레이션
5. **Small 변경합니다**: Break into small, incremental steps
6. **모니터**: Watch 위한 오류 동안 배포
7. **Document**: Explain 왜 및 어떻게
8. **Idempotent**: Migrations should be rerunnable

## 일반적인 Pitfalls

- Not 테스트 롤백 절차
- Making breaking 변경합니다 없이 downtime 전략
- Forgetting 에 handle NULL 값
- Not considering 인덱스 성능
- Ignoring foreign 키 constraints
- Migrating 또한 much 데이터 에서 once
