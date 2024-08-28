document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/players')
        .then(response => response.json())
        .then(players => {
            const player1Select = document.getElementById('player1');
            const player2Select = document.getElementById('player2');

            players.forEach(player => {
                const option1 = document.createElement('option');
                option1.value = player.id;
                option1.textContent = player.name;
                player1Select.appendChild(option1);

                const option2 = document.createElement('option');
                option2.value = player.id;
                option2.textContent = player.name;
                player2Select.appendChild(option2);
            });
        });
});
