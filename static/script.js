document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const name = document.getElementById('pokemon-name').value.toLowerCase();

    fetch(`/api/pokemon/${name}`)
        .then(response => response.json())
        .then(data => {
            console.log("Nombre del Pokémon buscado:", name);
            console.log("Data recibida:", data);  // 🔍 DEBUG

            const info = document.getElementById('pokemon-info');

            // Asegurar que los valores existen antes de usar .join()
            const types = Array.isArray(data.types) ? data.types.join(", ") : "Unknown";
            const abilities = Array.isArray(data.abilities) ? data.abilities.join(", ") : "Unknown";

            if (data.name) {  
                info.innerHTML = `
                    <p>${data.name.toUpperCase()} - Height: ${data.height}, Weight: ${data.weight}</p>
                    <p>Types: ${types}</p>
                    <p>Abilities: ${abilities}</p>
                    <button onclick="savePokemon('${data.name}', ${data.height}, ${data.weight}, '${types}', '${abilities}')">Save</button>
                `;
            } else {
                info.innerHTML = `<p style="color:red;">Error al obtener el Pokémon. Intenta de nuevo.</p>`;
            }
        })
        .catch(error => console.error("Error en la petición:", error));
});


function savePokemon(name, height, weight, types, abilities) {
    const pokemonData = {
        name: name,
        height: height,
        weight: weight,
        types: types.split(", ").filter(t => t !== "Unknown"), // Convertir a lista
        abilities: abilities.split(", ").filter(a => a !== "Unknown") // Convertir a lista
    };

    console.log("✅ JSON que se enviará:", JSON.stringify(pokemonData, null, 2));  // 🔍 DEBUG

    fetch('/api/pokemon/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(pokemonData)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.detail || "Error al guardar Pokémon"); });
        }
        return response.json();
    })
    .then(result => {
        alert("✅ Pokémon guardado exitosamente!");
        console.log("✅ Respuesta de la API:", result);
    })
    .catch(error => {
        console.error("❌ Error al guardar Pokémon:", error);
        alert(`❌ Error: ${error.message}`);
    });
}
