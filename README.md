# shorten-url

유저로부터 긴 url값을 받아 짧은 key값으로 교체 한 후 짧은 url을 리턴해주고 해당 url을 통해 원본 url로 리다이렉트 해주는 api입니다.

 

## 사용기술

* Backend: fastapi
* Database: sqlite

backend는 fastapi를 database는 sqlite를 사용하여 구현했습니다.

database의 경우 비교적 잦은 update와 delete를 생각해 nosql보다는 rdb를 쓰는것이 더 적절하다고 생각했고

다른 사용자의 테스트 상황을 고려해서 추가적은 db 설치 및 db 유저를 따로 생성 할 필요없이 간편하게 테스트가 가능은 sqlite를 사용했습니다.



## 요구사항

* python >= 3.12



## 구현 기능 설명

* **POST** /shorten

  유저로부터 url값과 expiratiin_hour를 받아 짧은 url을 리턴해주는 api입니다.

  hash를 통해 암호화를 진행했고 시도할때마다 다른값이 나오도록 시간값을 붙여 hash했습니다.
  
  * request data
  
    만료 시간은 hour 단위이고 입력하지 않으면 14일을 기본으로 합니다. 입력값을 24시간 이상, 1년 이하의 값으로 변환합니다.
  
    ```
    {
    	"url": <str> required,
    	"expiration_hour": <int> optional = 14 * 24
    }
    ```

  * response
  
    * 200 OK
  
      요청한 url이 이미 datadase에 존재하면 해당 데이터를 반환하고 없다면 새로운 shorten_key를 생성하고 반환합니다. host와 port는 실행 환경에 따라 유동적으로 반환합니다.
      
      ```
      {
      	"short_url": "http://localhost:8000/S5ten34KjT"
      }
      ```
      
    * 400 Bad Request
  
      요청한 url을 활용해 shorten_key를 생성합니다. 해당 과정에서 생성된 key가 이미 database에서 사용중이라면 다시 시도하고 5번의 short_key 생성 시도 끝에 중복되지 않는 key를 생성하지 못했을 경우 해당 결과를 반환합니다.
  
      ```
      "retry please"
      ```
    
      
    
    
    
    



## 설치방법

필요한 라이브러리는 텍스트 파일로 만들어 두었습니다.

```bash
$ pip install -r requirements.txt
```



## 실행방법

서버 실행과 api 테스트 실행을 분리해 두었습니다. 

* 서버 실행

```bash
$ cd app

$ uvicorn main:app
```



* 테스트 실행

test_가 붙은 테스트용 파이썬 파일이 자동으로 실행됩니다.

```bash
$ cd app

$ pytest
```



## swagger

fastapi의 경우 자동으로 swagger 문서를 생성합니다. 서버 실행 후 서버가 사용중인 port를 확인하고 아래 url를 통해 접속 가능합니다.

```
localhost:8000/docs#
```









