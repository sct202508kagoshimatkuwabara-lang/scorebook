document.addEventListener('DOMContentLoaded', function() {
    const addPitchButton = document.getElementById('add-pitch');
    const addBattingButton = document.getElementById('add-batting');

    if (addPitchButton) {
        addPitchButton.addEventListener('click', function() {
            // New pitch row addition logic here
            let newRow = document.createElement('tr');
            newRow.innerHTML = `
                <td><input type="text" name="pitch_type_new" placeholder="球種"></td>
                <td><input type="number" name="speed_new" placeholder="球速"></td>
                <td><input type="text" name="pitch_result_new" placeholder="結果"></td>
            `;
            document.getElementById('pitch-table').appendChild(newRow);
        });
    }

    if (addBattingButton) {
        addBattingButton.addEventListener('click', function() {
            // New batting row addition logic here
            let newRow = document.createElement('tr');
            newRow.innerHTML = `
                <td><input type="text" name="batter_name_new" placeholder="選手名"></td>
                <td><input type="text" name="batter_result_new" placeholder="結果"></td>
            `;
            document.getElementById('batting-table').appendChild(newRow);
        });
    }
});
