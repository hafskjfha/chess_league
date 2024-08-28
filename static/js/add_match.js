document.addEventListener('DOMContentLoaded', () => {
    const whitePlayerSelect = document.getElementById('whitePlayer');
    const blackPlayerSelect = document.getElementById('blackPlayer');

    // Players dropdown populate
    fetch('/api/players')
        .then(response => response.json())
        .then(data => {
            data.forEach(player => {
                const option = document.createElement('option');
                option.value = player.id;
                option.textContent = player.name;
                whitePlayerSelect.appendChild(option);

                const optionClone = option.cloneNode(true);
                blackPlayerSelect.appendChild(optionClone);
            });
        });

    // Form submission
    const form = document.getElementById('addMatchForm');
    form.addEventListener('submit', event => {
        event.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        fetch('/api/add_match', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(() => {
            alert('Match added successfully!');
            form.reset();
        });
    });
});
