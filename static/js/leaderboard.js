document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/leaderboard')
        .then(response => response.json())
        .then(data => {
            const leaderboard = document.getElementById('leaderboard');
            data.forEach(player => {
                const li = document.createElement('li');
                li.textContent = `${player.name}: ${player.wins} Wins, ${player.draws} Draws, ${player.losses} Losses`;
                leaderboard.appendChild(li);
            });
        });
});
