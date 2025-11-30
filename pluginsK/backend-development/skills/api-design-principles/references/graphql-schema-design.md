# GraphQL 스키마 설계 패턴

## 스키마 조직

### 모듈식 스키마 구조
```graphql
# user.graphql
type User {
  id: ID!
  email: String!
  name: String!
  posts: [Post!]!
}

extend type Query {
  user(id: ID!): User
  users(first: Int, after: String): UserConnection!
}

extend type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

# post.graphql
type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
}

extend type Query {
  post(id: ID!): Post
}
```

## 유형 설계 패턴

### 1. Non-Null 유형
```graphql
type User {
  id: ID!              # Always required
  email: String!       # Required
  phone: String        # Optional (nullable)
  posts: [Post!]!      # Non-null array of non-null posts
  tags: [String!]      # Nullable array of non-null strings
}
```

### 2. 인터페이스 위한 Polymorphism
```graphql
interface Node {
  id: ID!
  createdAt: DateTime!
}

type User implements Node {
  id: ID!
  createdAt: DateTime!
  email: String!
}

type Post implements Node {
  id: ID!
  createdAt: DateTime!
  title: String!
}

type Query {
  node(id: ID!): Node
}
```

### 3. Unions 위한 Heterogeneous Results
```graphql
union SearchResult = User | Post | Comment

type Query {
  search(query: String!): [SearchResult!]!
}

# Query example
{
  search(query: "graphql") {
    ... on User {
      name
      email
    }
    ... on Post {
      title
      content
    }
    ... on Comment {
      text
      author { name }
    }
  }
}
```

### 4. 입력 유형
```graphql
input CreateUserInput {
  email: String!
  name: String!
  password: String!
  profileInput: ProfileInput
}

input ProfileInput {
  bio: String
  avatar: String
  website: String
}

input UpdateUserInput {
  id: ID!
  email: String
  name: String
  profileInput: ProfileInput
}
```

## Pagination 패턴

### Relay Cursor Pagination (권장됨)
```graphql
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type Query {
  users(
    first: Int
    after: String
    last: Int
    before: String
  ): UserConnection!
}

# Usage
{
  users(first: 10, after: "cursor123") {
    edges {
      cursor
      node {
        id
        name
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### 오프셋 Pagination (Simpler)
```graphql
type UserList {
  items: [User!]!
  total: Int!
  page: Int!
  pageSize: Int!
}

type Query {
  users(page: Int = 1, pageSize: Int = 20): UserList!
}
```

## Mutation 설계 패턴

### 1. 입력/페이로드 패턴
```graphql
input CreatePostInput {
  title: String!
  content: String!
  tags: [String!]
}

type CreatePostPayload {
  post: Post
  errors: [Error!]
  success: Boolean!
}

type Error {
  field: String
  message: String!
  code: String!
}

type Mutation {
  createPost(input: CreatePostInput!): CreatePostPayload!
}
```

### 2. Optimistic 응답 지원
```graphql
type UpdateUserPayload {
  user: User
  clientMutationId: String
  errors: [Error!]
}

input UpdateUserInput {
  id: ID!
  name: String
  clientMutationId: String
}

type Mutation {
  updateUser(input: UpdateUserInput!): UpdateUserPayload!
}
```

### 3. Batch Mutations
```graphql
input BatchCreateUserInput {
  users: [CreateUserInput!]!
}

type BatchCreateUserPayload {
  results: [CreateUserResult!]!
  successCount: Int!
  errorCount: Int!
}

type CreateUserResult {
  user: User
  errors: [Error!]
  index: Int!
}

type Mutation {
  batchCreateUsers(input: BatchCreateUserInput!): BatchCreateUserPayload!
}
```

## 분야 설계

### 인수 및 필터링
```graphql
type Query {
  posts(
    # Pagination
    first: Int = 20
    after: String

    # Filtering
    status: PostStatus
    authorId: ID
    tag: String

    # Sorting
    orderBy: PostOrderBy = CREATED_AT
    orderDirection: OrderDirection = DESC

    # Searching
    search: String
  ): PostConnection!
}

enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

enum PostOrderBy {
  CREATED_AT
  UPDATED_AT
  TITLE
}

enum OrderDirection {
  ASC
  DESC
}
```

### 계산된 필드
```graphql
type User {
  firstName: String!
  lastName: String!
  fullName: String!  # Computed in resolver

  posts: [Post!]!
  postCount: Int!    # Computed, doesn't load all posts
}

type Post {
  likeCount: Int!
  commentCount: Int!
  isLikedByViewer: Boolean!  # Context-dependent
}
```

## Subscriptions

```graphql
type Subscription {
  postAdded: Post!

  postUpdated(postId: ID!): Post!

  userStatusChanged(userId: ID!): UserStatus!
}

type UserStatus {
  userId: ID!
  online: Boolean!
  lastSeen: DateTime!
}

# Client usage
subscription {
  postAdded {
    id
    title
    author {
      name
    }
  }
}
```

## 사용자 정의 Scalars

```graphql
scalar DateTime
scalar Email
scalar URL
scalar JSON
scalar Money

type User {
  email: Email!
  website: URL
  createdAt: DateTime!
  metadata: JSON
}

type Product {
  price: Money!
}
```

## 지시문

### 구축된-에서 지시문
```graphql
type User {
  name: String!
  email: String! @deprecated(reason: "Use emails field instead")
  emails: [String!]!

  # Conditional inclusion
  privateData: PrivateData @include(if: $isOwner)
}

# Query
query GetUser($isOwner: Boolean!) {
  user(id: "123") {
    name
    privateData @include(if: $isOwner) {
      ssn
    }
  }
}
```

### 사용자 정의 지시문
```graphql
directive @auth(requires: Role = USER) on FIELD_DEFINITION

enum Role {
  USER
  ADMIN
  MODERATOR
}

type Mutation {
  deleteUser(id: ID!): Boolean! @auth(requires: ADMIN)
  updateProfile(input: ProfileInput!): User! @auth
}
```

## 오류 처리

### Union 오류 패턴
```graphql
type User {
  id: ID!
  email: String!
}

type ValidationError {
  field: String!
  message: String!
}

type NotFoundError {
  message: String!
  resourceType: String!
  resourceId: ID!
}

type AuthorizationError {
  message: String!
}

union UserResult = User | ValidationError | NotFoundError | AuthorizationError

type Query {
  user(id: ID!): UserResult!
}

# Usage
{
  user(id: "123") {
    ... on User {
      id
      email
    }
    ... on NotFoundError {
      message
      resourceType
    }
    ... on AuthorizationError {
      message
    }
  }
}
```

### 오류 에서 페이로드
```graphql
type CreateUserPayload {
  user: User
  errors: [Error!]
  success: Boolean!
}

type Error {
  field: String
  message: String!
  code: ErrorCode!
}

enum ErrorCode {
  VALIDATION_ERROR
  UNAUTHORIZED
  NOT_FOUND
  INTERNAL_ERROR
}
```

## N+1 쿼리 문제 Solutions

### DataLoader 패턴
```python
from aiodataloader import DataLoader

class PostLoader(DataLoader):
    async def batch_load_fn(self, post_ids):
        posts = await db.posts.find({"id": {"$in": post_ids}})
        post_map = {post["id"]: post for post in posts}
        return [post_map.get(pid) for pid in post_ids]

# Resolver
@user_type.field("posts")
async def resolve_posts(user, info):
    loader = info.context["loaders"]["post"]
    return await loader.load_many(user["post_ids"])
```

### 쿼리 Depth 제한하는
```python
from graphql import GraphQLError

def depth_limit_validator(max_depth: int):
    def validate(context, node, ancestors):
        depth = len(ancestors)
        if depth > max_depth:
            raise GraphQLError(
                f"Query depth {depth} exceeds maximum {max_depth}"
            )
    return validate
```

### 쿼리 Complexity 분석
```python
def complexity_limit_validator(max_complexity: int):
    def calculate_complexity(node):
        # Each field = 1, lists multiply
        complexity = 1
        if is_list_field(node):
            complexity *= get_list_size_arg(node)
        return complexity

    return validate_complexity
```

## 스키마 Versioning

### 분야 Deprecation
```graphql
type User {
  name: String! @deprecated(reason: "Use firstName and lastName")
  firstName: String!
  lastName: String!
}
```

### 스키마 Evolution
```graphql
# v1 - Initial
type User {
  name: String!
}

# v2 - Add optional field (backward compatible)
type User {
  name: String!
  email: String
}

# v3 - Deprecate and add new field
type User {
  name: String! @deprecated(reason: "Use firstName/lastName")
  firstName: String!
  lastName: String!
  email: String
}
```

## 최선의 관행 Summary

1. **Nullable vs Non-Null**: Start nullable, make non-null 때 보증된
2. **입력 유형**: 항상 use 입력 유형 위한 mutations
3. **페이로드 패턴**: 반환 오류 에서 mutation 페이로드
4. **Pagination**: Use cursor-based 위한 무한 scroll, 오프셋 위한 간단한 cases
5. **Naming**: Use camelCase 위한 필드, PascalCase 위한 유형
6. **Deprecation**: Use `@deprecated` instead of removing 필드
7. **DataLoaders**: 항상 use 위한 관계 에 prevent N+1
8. **Complexity 제한합니다**: Protect against expensive 쿼리
9. **사용자 정의 Scalars**: Use 위한 도메인-특정 유형 (Email, 날짜시간)
10. **문서화**: Document 모든 필드 와 함께 descriptions
