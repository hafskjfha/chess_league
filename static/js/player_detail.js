document.addEventListener('DOMContentLoaded', () => {
    const playerId = window.location.pathname.split('/').pop();

    fetch(`/api/player/${playerId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('playerName').textContent = data.name;
            document.getElementById('playerWins').textContent = data.wins;
            document.getElementById('playerDraws').textContent = data.draws;
            document.getElementById('playerLosses').textContent = data.losses;

            const recentMatches = document.getElementById('recentMatches');
            data.matches.slice(-10).forEach(match => {
                const li = document.createElement('li');
                li.textContent = `${match.date}: ${match.white_player} vs ${match.black_player} - ${match.result}`;
                recentMatches.appendChild(li);
            });
        });
});
