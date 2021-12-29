# Moominstagram

Sparta Coding Camp - Team Proejct 1. Instagram Clone Coding
<br>
<br>

## 😎 무민과아이들 
* [윤소현님](https://github.com/YoonSeohyeon) (팀장)
* [이병준님](https://github.com/dugadak)
* [한장원님](https://github.com/HANJANGWON)
* [이용헌님](https://github.com/yongheon-Lee)
* [박재영님](https://github.com/devjcode)  

<br>
<br>

## 🦴 개발 포지션
+ Front-end : 윤소현, 이병준, 이용헌
+ Back-end : 한장원, 박재영  

<br>
<br>

## 📆 프로젝트 기간
2021-12-28 ~ 2021.01.04  
<br>
<br>
## 🤖 기술 스택
1. Front : HTML, JavaScript, Ajax
2. Back : Python, Flask, MongoDB
3. Server : AWS EC2
4. 협업 : [github](https://github.com/MoominAndChildrenTeam/), [Figma](https://www.figma.com/file/bxfXRmb2SybXbWdoB3PudW/%EB%AC%B4%EB%AF%BC?node-id=0%3A1)

<br>
<br>

## 🕸 아키텍처  
<img width="1152" alt="Frame 1" src="https://user-images.githubusercontent.com/87844396/147567865-c06f25c0-dfbc-499d-bc5c-7957a1ab35ef.png">
<br>
<br>

## 🙉 구현
- 로그인
- 회원가입
- 메인페이지
  + 전체 글 조회
- 마이페이지
  + 자신이 쓴 글 모아보기
  + 팔로우 팔로워 수 보기  

<br>
<br>

## 🎈 DB 스키마  
|기능|method|url|request|response|
|---|---|---|---|---|
|메인화면|GET|/|로그인 되어있지 않을시 /login 으로|
|로그인|POST|/login|{'email':email, 'pw':pw}|
|회원가입|POST|/register|{'email':email, 'pw':pw}||
|이메일인증|POST|/register2|.|.|
|CRUD|.|.|.|.|
|메인화면|GET|/|{...}|
|마이페이지|GET|/my_page|{...}|
|업로드|POST|/upload_page|{'date':date, 'image':image_receive, 'comment':comment_receive}|
<br>
<br>


