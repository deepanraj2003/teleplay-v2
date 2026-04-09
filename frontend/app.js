const API = window.location.origin;

async function loadMovies() {
    const res = await fetch(`${API}/api/movies`);
    const data = await res.json();

    const container = document.getElementById("movies");

    data.forEach(movie => {
        const div = document.createElement("div");

        div.innerHTML = `
            <h3>${movie.name}</h3>
            <a href="/player?file_id=${movie.file_id}">
                Watch
            </a>
        `;

        container.appendChild(div);
    });
}

loadMovies();
