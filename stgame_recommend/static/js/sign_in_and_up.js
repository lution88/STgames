const signUpButton = document.getElementById("sign-up");
const signInButton = document.getElementById("sign-in");
const container = document.getElementById("container");

signUpButton.addEventListener("click", () => {
    container.classList.add("right-panel-active");
});

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

$('.email-check-btn').click(function (){
    const email = $('#email').val()
    if (email === ''){
        alert('이메일 입력 좀...!!!!')
    }

    $.ajax({
        type: 'GET',
        url: '/email-check?email=' + email,
        datatype: 'json',
        success: function (response){
            if (response.result !== 'success') {
                alert(response.data)
                return
            }
            if (response.data === 'exist') {
                alert('그 이메일은 이미 있소!')
                $('#email').val('').focus()
            } else {
                alert('좋아, 사용 가능하군!!')
            }
        }
    })
})