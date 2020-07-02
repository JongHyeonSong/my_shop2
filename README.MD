# 강아지, 고양이 반려용품 판매 사이트 제작
<img width="439" alt="대시보드" src="readMeImg/admin/dashboard.png">

> myshop 웹페이지는 반려견, 반려용품 판매 사이트 입니다  
관리자 레벨에서는 실시간으로 고객의 주문을 대시보드에서 관리/수정/삭제 할수있고  
고객은 원하는 물품을 주문하고 본인 Profile을 꾸밀 수 있습니다
### 필요한 기능
- 장고ORM을 이용한 기본적인 CRUD
- 관리자 모드와 일반사용자 모드를 나누어서 url을 변경해주고 template을 다르게 랜더링 해주기
- 위 사항을 views 로직 내에서 구현시에 코드 가독성, 중복 현상이 일어나므로 decorator를 이용하기
- 장고 시그널을 이용해 User모델에서 save()가 발동 되었을때 user의 소속 group을 정하고 1:1매칭 되어있는 Customer을 새로 생성해주기
- 각 고객들마다 개인 profile 설정 템플릿 만들기
- 장고 내장함수인 login/logout 이용해 로그인 로그아웃 템플릿만들기, 에러/성공 메세지 띄우기,bootstrap 이용해 간단한 디자인하기

# 모델 구성
> 총 4가지 모델을 만들었으며 1:1/1:다/다:다 관계를 장고 ORM으로 구현하였습니다  
  - Customer 모델의 user를 장고에서 기본제공하는 User모델과 1:1관계를 맺어 장고에서 제공하는 login/logout 세션관리를 이용해 개발기간을 단축시켰습니다
  <img width="439" alt="고객모델" src="readMeImg/model/customer.png">

  - 하나의 제품은 여러가지 태그를 가질수 있고 또 하나의 태그 또한 여러가지 제품군을 가지고 있을수 있습니다. ManyToMany필드를 통해 마이그레이션 하게되면 각각의 pk를 로우의 값으로 하는 테이블이 자동으로 생성됩니다
  <img width="439" alt="다대다관계" src="readMeImg/model/product-tag.png">
  
  
# 판매중인 아이템 CRUD 하기
  <img width="439" alt="order폼" src="readMeImg/form/order.png">
  <img width="439" alt="update뷰" src="readMeImg/view/update.png">  

  넷중에 상대적으로 어려운 기존의 값을 바꾸는 update뷰 입니다  
  주문 모델로 간단하게 form을 만드는 강력한 기능을 제공해주어서 템플릿단에서  
  POST메세지를 보냈을때 조건문으로 분기를시키고  
  POST자료와 기존 자료를 인자로해서 유효성 검사후 저장합니다
  POST자료만 받아서 save()를 실행 했을경우는 기존에 있던 자료를 그대로 놔두고 새로 생성하므로 덮어쓰기위해 POST자료와 원래 order를 모두 인자로 날려주어야 새로 db가 덮어써집니다
  
# decorator를 이용한 권한 설정
  
장고에서는 **login_required** 라는 데코레이터로 로그인 User테이블에 있는 사람으로 로그인 되어있지 않다면 자동으로 특정 url로 보낼수있는 데코레이터를 제공합니다  
비슷한 원리로 자기만의 decorator역시 만들수 있습니다
<img width="439" alt="update뷰" src="readMeImg/decorator/unauthenticated.png">  
장고 user는 지금이 게스트상태인지 login상태인지를 알려주는 'is_authenticated' 인자를 가지고 있으므로 분기처리를 하여 이미 로그인된 사람은 redirect 함수로 다른곳으로 보내고 그 이외의 경우에는 본래 함수를 실행하게 합니다
<img width="439" alt="update뷰" src="readMeImg/view/login.png">  
다음과같이 login페이지에 login 되어있는 유저가 접근하려고하면 decorator함수로 인해서 바로 'home'으로 렌더링되게 됩니다  
<img width="439" alt="update뷰" src="readMeImg/view/login_1.png">  
위와 같이 데코레이터를 사용하지 않고 해당 로직을 views에서 처리할 수도 있지만 분기문 때문에 코드가 쓸데없이 지저분해지고 또 재사용하기가 번거롭게 됩니다


# 장고 signal을 사용해 이벤트 일괄 처리하기
