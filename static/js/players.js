document.addEventListener('DOMContentLoaded', () => {
    const playerList = document.getElementById('playerList');

    fetch('/api/players')
        .then(response => response.json())
        .then(data => {
            data.forEach(player => {
                const li = document.createElement('li');
                const detailLink = document.createElement('a');
                detailLink.href = `/player_detail/${player.id}`;
                detailLink.textContent = player.name;
                li.appendChild(detailLink);
                playerList.appendChild(li);
            });
        });

    const addPlayerBtn = document.getElementById('addPlayerBtn');
    addPlayerBtn.addEventListener('click', () => {
        const playerName = prompt('Enter player name:');
        if (playerName) {
            fetch('/api/add_player', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name: playerName })
            })
            .then(response => response.json())
            .then(() => location.reload());
        }
    });
});
