function transitionToPage(url) {
    document.body.classList.add('slide-out');
    setTimeout(function() {
        window.location.href = url;
    }, 500); // 0.5초 후에 페이지 전환
}

// 슬라이드 전환 애니메이션 스타일
document.head.insertAdjacentHTML(
    'beforeend',
    '<style>' +
        '.slide-out { animation: slideOut 0.5s forwards; }' +
        '@keyframes slideOut { from { transform: translateX(0); opacity: 1; } to { transform: translateX(-100%); opacity: 0; } }' +
    '</style>'
);

