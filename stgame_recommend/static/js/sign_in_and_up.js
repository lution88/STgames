const signUpButton = document.getElementById("sign-up");
const signInButton = document.getElementById("sign-in");
const container = document.getElementById("container");

// 회원가입 폼으로 넘어가는 버튼
signUpButton.addEventListener("click", () => {
    container.classList.add("right-panel-active");
});

// 로그인 폼으로 넘어가는 버튼
signInButton.addEventListener("click", () => {
    container.classList.remove("right-panel-active");
});

// 아이디 찾기 모달 열기
const modalId = document.getElementById("modal-find-id");
const buttonFindId = document.getElementById("find-id");
buttonFindId.addEventListener("click", e => {
    modalId.style.top = window.pageYOffset + 'px'
    modalId.style.display = "flex";
    document.body.style.overflowY = 'hidden'; // 스크롤 없애기
});

// 모달 닫기
const buttonCloseModalId = document.getElementById('close-modal-id');
buttonCloseModalId.addEventListener('click', e => {
    modalId.style.display = 'none';
    document.body.style.overflowY = 'visible';
});

// 비밀번호 찾기 모달 열기
const modalPw = document.getElementById("modal-find-pw");
const buttonFindPw = document.getElementById("find-pw");
buttonFindPw.addEventListener("click", e => {
    modalPw.style.top = window.pageYOffset + 'px'
    modalPw.style.display = "flex";
    document.body.style.overflowY = 'hidden'; // 스크롤 없애기
});

// 모달 닫기
const buttonCloseModalPw = document.getElementById('close-modal-pw');
buttonCloseModalPw.addEventListener('click', e => {
    modalPw.style.display = 'none';
    document.body.style.overflowY = 'visible';
});

// 아이디 중복 확인 및 유효성 검사
$('.id-check-btn').click(function () {
    const username = $('#username').val()
    if (username === '') {
        alert('빈칸은 채워 주세요!')
        $('.id').css('border','3px solid red')
        return
    }

    $.ajax({
        type: 'POST',
        url: '/id-check/',
        data: {username: username},
        datatype: 'json',
        success: function (response) {
            if (response.result !== 'success') {
                alert('올바른 아이디를 적어 주세요!')
                $('.id').css('border','3px solid red')
                return
            }

            if (response.data === 'exist') {
                alert('다른 아이디를 사용해 주세요!')
                $('#username').val('').focus()
            } else {
                alert('사용 가능한 아이디입니다!')
            }
        }
    })
})


// 이메일 중복 확인 및 유효성 검사
$('.email-check-btn').click(function () {
    const email = $('#email').val()
    if (email === '') {
        alert('빈칸은 채워 주세요!')
        $('.email').css('border','3px solid red')
        return
    }

    $.ajax({
        type: 'POST',
        url: '/email-check/',
        data: {email: email},
        datatype: 'json',
        success: function (response) {
            if (response.result !== 'success') {
                alert('올바른 메일을 적어 주세요!')
                $('.email').css('border','3px solid red')
                return
            }

            if (response.data === 'exist') {
                alert('다른 메일을 사용해 주세요!')
                $('#email').val('')
            } else {
                alert('사용 가능한 메일입니다!')
            }
        }
    })
})