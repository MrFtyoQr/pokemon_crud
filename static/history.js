document.addEventListener("DOMContentLoaded", function () {
    loadHistory();
});

function loadHistory() {
    fetch('/api/pokemon/saved')
        .then(response => response.json())
        .then(data => {
            console.log("Pokémon guardados:", data); // 🔍 Debug
            
            if (!Array.isArray(data)) {
                console.error("❌ Error: Respuesta inesperada:", data);
                return;
            }

            const list = document.getElementById('history-list');
            list.innerHTML = '';

            data.forEach(pokemon => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `
                    <strong>${pokemon.name.toUpperCase()}</strong> - Altura: ${pokemon.height}, Peso: ${pokemon.weight}
                    <button onclick="deletePokemon('${pokemon._id}', '${pokemon._rev}')">Eliminar</button>
                    <button onclick="editPokemon('${pokemon._id}', '${pokemon._rev}', '${pokemon.name}', ${pokemon.height}, ${pokemon.weight})">Editar</button>
                `;
                list.appendChild(listItem);
            });
        })
        .catch(error => console.error("❌ Error al obtener el historial:", error));
}


function deletePokemon(id, rev) {
    fetch(`/api/pokemon/delete/${id}/${rev}`, { method: 'DELETE' })
        .then(response => response.json())
        .then(result => {
            alert("Pokémon eliminado correctamente!");
            loadHistory(); // Recargar lista después de eliminar
        })
        .catch(error => console.error("❌ Error al eliminar Pokémon:", error));
}

function editPokemon(id, rev, name, height, weight) {
    const newHeight = prompt(`Editar altura de ${name}:`, height);
    const newWeight = prompt(`Editar peso de ${name}:`, weight);

    if (newHeight !== null && newWeight !== null) {
        const updatedData = {
            name: name,
            height: parseInt(newHeight),
            weight: parseInt(newWeight),
            types: [],
            abilities: [],
            _rev: rev
        };

        fetch(`/api/pokemon/update/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedData)
        })
        .then(response => response.json())
        .then(result => {
            alert("Pokémon actualizado correctamente!");
            loadHistory(); // Recargar lista después de actualizar
        })
        .catch(error => console.error("❌ Error al actualizar Pokémon:", error));
    }
}
