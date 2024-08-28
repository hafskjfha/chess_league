document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/matches')
        .then(response => response.json())
        .then(data => {
            const matchList = document.getElementById('matchList');
            data.forEach(match => {
                const li = document.createElement('li');
                const detailLink = document.createElement('a');
                detailLink.href = `/match_detail/${match.id}`;
                detailLink.textContent = `${match.date}: ${match.white_player} vs ${match.black_player} - ${match.result}`;
                li.appendChild(detailLink);
                matchList.appendChild(li);
            });
        });
});
