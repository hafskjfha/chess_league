document.addEventListener('DOMContentLoaded', () => {
    const matchId = window.location.pathname.split('/').pop();

    fetch(`/api/match/${matchId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('whitePlayer').textContent = data.white_player;
            document.getElementById('blackPlayer').textContent = data.black_player;
            document.getElementById('result').textContent = data.result;
            document.getElementById('date').textContent = data.date;
            document.getElementById('resultInfo').textContent = data.result_info;

            const gameLink = document.getElementById('gameLink');
            gameLink.href = `https://${data.game_link}`; // 여기서 https://를 붙여 절대 경로로 변환

            const gameFrame = document.getElementById('gameFrame');
            gameFrame.src = `https://${data.game_link}`; // https://를 붙여 절대 경로로 설정
        });
});

