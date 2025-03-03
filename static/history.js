document.addEventListener("DOMContentLoaded", function () {
    loadHistory();
});

function loadHistory() {
    fetch('/api/pokemon/saved')
        .then(response => response.json())
        .then(data => {
            console.log("Pokémon guardados:", data);
            
            if (!Array.isArray(data)) {
                console.error("❌ Error: Respuesta inesperada:", data);
                return;
            }

            const list = document.getElementById('history-list');
            list.innerHTML = '';

            data.forEach(pokemon => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `
                    <strong>${pokemon.name.toUpperCase()}</strong> - 
                    Altura: ${pokemon.height}, Peso: ${pokemon.weight}, 
                    Tipos: ${pokemon.types.join(", ")}, 
                    Habilidades: ${pokemon.abilities.join(", ")}
                    <button onclick="deletePokemon('${pokemon._id}', '${pokemon._rev}')">Eliminar</button>
                    <button onclick="editPokemon('${pokemon._id}', '${pokemon._rev}', '${pokemon.name}', ${pokemon.height}, ${pokemon.weight}, '${pokemon.types.join(", ")}', '${pokemon.abilities.join(", ")}')">Editar</button>
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
            loadHistory(); 
        })
        .catch(error => console.error("❌ Error al eliminar Pokémon:", error));
}

async function editPokemon(id, rev, name, height, weight, types, abilities) {
    const newName = prompt(`Editar nombre de ${name}:`, name);
    const newHeight = prompt(`Editar altura de ${name}:`, height);
    const newWeight = prompt(`Editar peso de ${name}:`, weight);
    const newTypes = prompt(`Editar tipos de ${name} (separados por comas):`, types);
    const newAbilities = prompt(`Editar habilidades de ${name} (separadas por comas):`, abilities);

    if (newName !== null && newHeight !== null && newWeight !== null && newTypes !== null && newAbilities !== null) {
        const updatedData = {
            name: newName.trim(),
            height: parseFloat(newHeight),
            weight: parseFloat(newWeight),
            types: newTypes.split(",").map(t => t.trim()),  // Convertir a lista
            abilities: newAbilities.split(",").map(a => a.trim()),  // Convertir a lista
            _rev: rev
        };

        try {
            const response = await fetch(`/api/pokemon/update/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updatedData)
            });

            if (response.ok) {
                alert("Pokémon actualizado correctamente!");
                loadHistory(); // Recargar la lista para reflejar los cambios
            } else {
                alert("❌ Error al actualizar el Pokémon.");
            }
        } catch (error) {
            console.error("❌ Error al actualizar Pokémon:", error);
        }
    } else {
        alert("Edición cancelada o valores inválidos.");
    }
}
