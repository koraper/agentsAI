---
name: angular-migration
description: Migrate 에서 AngularJS 에 Angular 사용하여 하이브리드 최빈값, incremental 컴포넌트 rewriting, 및 종속성 인젝션 업데이트합니다. Use 때 upgrading AngularJS 애플리케이션, 계획 프레임워크 migrations, 또는 modernizing 레거시 Angular 코드.
---

# Angular 마이그레이션

마스터 AngularJS 에 Angular 마이그레이션, 포함하여 하이브리드 apps, 컴포넌트 변환, 종속성 인젝션 변경합니다, 및 라우팅 마이그레이션.

## 때 에 Use This Skill

- Migrating AngularJS (1.x) 애플리케이션 에 Angular (2+)
- 실행 중 하이브리드 AngularJS/Angular 애플리케이션
- Converting 지시문 에 컴포넌트
- Modernizing 종속성 인젝션
- Migrating 라우팅 시스템
- Updating 에 최신 Angular 버전
- Implementing Angular 최선의 관행

## 마이그레이션 Strategies

### 1. Big Bang (완전한 Rewrite)
- Rewrite entire app 에서 Angular
- 병렬로 개발
- switch over 에서 once
- **최선의 위한:** Small apps, green 분야 projects

### 2. Incremental (하이브리드 접근법)
- Run AngularJS 및 Angular side-에 의해-side
- Migrate 기능 에 의해 기능
- ngUpgrade 위한 interop
- **최선의 위한:** Large apps, continuous 전달

### 3. Vertical 슬라이스
- Migrate one 기능 완전히
- 새로운 기능 에서 Angular, maintain 오래된 에서 AngularJS
- 점진적으로 replace
- **최선의 위한:** Medium apps, 구별되는 기능

## 하이브리드 App 설정

```typescript
// main.ts - Bootstrap hybrid app
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { UpgradeModule } from '@angular/upgrade/static';
import { AppModule } from './app/app.module';

platformBrowserDynamic()
  .bootstrapModule(AppModule)
  .then(platformRef => {
    const upgrade = platformRef.injector.get(UpgradeModule);
    // Bootstrap AngularJS
    upgrade.bootstrap(document.body, ['myAngularJSApp'], { strictDi: true });
  });
```

```typescript
// app.module.ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { UpgradeModule } from '@angular/upgrade/static';

@NgModule({
  imports: [
    BrowserModule,
    UpgradeModule
  ]
})
export class AppModule {
  constructor(private upgrade: UpgradeModule) {}

  ngDoBootstrap() {
    // Bootstrapped manually in main.ts
  }
}
```

## 컴포넌트 마이그레이션

### AngularJS 컨트롤러 → Angular 컴포넌트
```javascript
// Before: AngularJS controller
angular.module('myApp').controller('UserController', function($scope, UserService) {
  $scope.user = {};

  $scope.loadUser = function(id) {
    UserService.getUser(id).then(function(user) {
      $scope.user = user;
    });
  };

  $scope.saveUser = function() {
    UserService.saveUser($scope.user);
  };
});
```

```typescript
// After: Angular component
import { Component, OnInit } from '@angular/core';
import { UserService } from './user.service';

@Component({
  selector: 'app-user',
  template: `
    <div>
      <h2>{{ user.name }}</h2>
      <button (click)="saveUser()">Save</button>
    </div>
  `
})
export class UserComponent implements OnInit {
  user: any = {};

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.loadUser(1);
  }

  loadUser(id: number) {
    this.userService.getUser(id).subscribe(user => {
      this.user = user;
    });
  }

  saveUser() {
    this.userService.saveUser(this.user);
  }
}
```

### AngularJS 지시문 → Angular 컴포넌트
```javascript
// Before: AngularJS directive
angular.module('myApp').directive('userCard', function() {
  return {
    restrict: 'E',
    scope: {
      user: '=',
      onDelete: '&'
    },
    template: `
      <div class="card">
        <h3>{{ user.name }}</h3>
        <button ng-click="onDelete()">Delete</button>
      </div>
    `
  };
});
```

```typescript
// After: Angular component
import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-user-card',
  template: `
    <div class="card">
      <h3>{{ user.name }}</h3>
      <button (click)="delete.emit()">Delete</button>
    </div>
  `
})
export class UserCardComponent {
  @Input() user: any;
  @Output() delete = new EventEmitter<void>();
}

// Usage: <app-user-card [user]="user" (delete)="handleDelete()"></app-user-card>
```

## 서비스 마이그레이션

```javascript
// Before: AngularJS service
angular.module('myApp').factory('UserService', function($http) {
  return {
    getUser: function(id) {
      return $http.get('/api/users/' + id);
    },
    saveUser: function(user) {
      return $http.post('/api/users', user);
    }
  };
});
```

```typescript
// After: Angular service
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor(private http: HttpClient) {}

  getUser(id: number): Observable<any> {
    return this.http.get(`/api/users/${id}`);
  }

  saveUser(user: any): Observable<any> {
    return this.http.post('/api/users', user);
  }
}
```

## 종속성 인젝션 변경합니다

### Downgrading Angular → AngularJS
```typescript
// Angular service
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class NewService {
  getData() {
    return 'data from Angular';
  }
}

// Make available to AngularJS
import { downgradeInjectable } from '@angular/upgrade/static';

angular.module('myApp')
  .factory('newService', downgradeInjectable(NewService));

// Use in AngularJS
angular.module('myApp').controller('OldController', function(newService) {
  console.log(newService.getData());
});
```

### Upgrading AngularJS → Angular
```typescript
// AngularJS service
angular.module('myApp').factory('oldService', function() {
  return {
    getData: function() {
      return 'data from AngularJS';
    }
  };
});

// Make available to Angular
import { InjectionToken } from '@angular/core';

export const OLD_SERVICE = new InjectionToken<any>('oldService');

@NgModule({
  providers: [
    {
      provide: OLD_SERVICE,
      useFactory: (i: any) => i.get('oldService'),
      deps: ['$injector']
    }
  ]
})

// Use in Angular
@Component({...})
export class NewComponent {
  constructor(@Inject(OLD_SERVICE) private oldService: any) {
    console.log(this.oldService.getData());
  }
}
```

## 라우팅 마이그레이션

```javascript
// Before: AngularJS routing
angular.module('myApp').config(function($routeProvider) {
  $routeProvider
    .when('/users', {
      template: '<user-list></user-list>'
    })
    .when('/users/:id', {
      template: '<user-detail></user-detail>'
    });
});
```

```typescript
// After: Angular routing
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  { path: 'users', component: UserListComponent },
  { path: 'users/:id', component: UserDetailComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
```

## 폼 마이그레이션

```html
<!-- Before: AngularJS -->
<form name="userForm" ng-submit="saveUser()">
  <input type="text" ng-model="user.name" required>
  <input type="email" ng-model="user.email" required>
  <button ng-disabled="userForm.$invalid">Save</button>
</form>
```

```typescript
// After: Angular (Template-driven)
@Component({
  template: `
    <form #userForm="ngForm" (ngSubmit)="saveUser()">
      <input type="text" [(ngModel)]="user.name" name="name" required>
      <input type="email" [(ngModel)]="user.email" name="email" required>
      <button [disabled]="userForm.invalid">Save</button>
    </form>
  `
})

// Or Reactive Forms (preferred)
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  template: `
    <form [formGroup]="userForm" (ngSubmit)="saveUser()">
      <input formControlName="name">
      <input formControlName="email">
      <button [disabled]="userForm.invalid">Save</button>
    </form>
  `
})
export class UserFormComponent {
  userForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.userForm = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]]
    });
  }

  saveUser() {
    console.log(this.userForm.value);
  }
}
```

## 마이그레이션 Timeline

```
Phase 1: Setup (1-2 weeks)
- Install Angular CLI
- Set up hybrid app
- Configure build tools
- Set up testing

Phase 2: Infrastructure (2-4 weeks)
- Migrate services
- Migrate utilities
- Set up routing
- Migrate shared components

Phase 3: Feature Migration (varies)
- Migrate feature by feature
- Test thoroughly
- Deploy incrementally

Phase 4: Cleanup (1-2 weeks)
- Remove AngularJS code
- Remove ngUpgrade
- Optimize bundle
- Final testing
```

## 리소스

- **참조/하이브리드-최빈값.md**: 하이브리드 app 패턴
- **참조/컴포넌트-마이그레이션.md**: 컴포넌트 변환 가이드
- **참조/종속성-인젝션.md**: DI 마이그레이션 strategies
- **참조/라우팅.md**: 라우팅 마이그레이션
- **자산/하이브리드-bootstrap.ts**: 하이브리드 app 템플릿
- **자산/마이그레이션-timeline.md**: Project 계획
- **스크립트/analyze-angular-app.sh**: App 분석 스크립트

## 최선의 관행

1. **Start 와 함께 서비스**: Migrate 서비스 첫 번째 (easier)
2. **Incremental 접근법**: 기능-에 의해-기능 마이그레이션
3. **Test 지속적으로**: Test 에서 모든 단계
4. **Use TypeScript**: Migrate 에 TypeScript early
5. **Follow 스타일 가이드**: Angular 스타일 가이드 에서 day 1
6. **Optimize Later**: Get it 작업, then optimize
7. **Document**: Keep 마이그레이션 notes

## 일반적인 Pitfalls

- Not 설정하는 하이브리드 app 올바르게
- Migrating UI 이전 logic
- Ignoring 변경 감지 differences
- Not 처리 범위 적절하게
- Mixing 패턴 (AngularJS + Angular)
- 부적절한 테스트
