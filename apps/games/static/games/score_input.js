document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.querySelector("#input-rows");
    const addRowBtn = document.querySelector("#add-row-btn");
    const gameId = document.querySelector("#game-id").value;

    // 行追加
    addRowBtn.addEventListener("click", () => {
        tableBody.insertAdjacentHTML("beforeend", createRow());
    });

    // イベントデリゲート：保存ボタンの処理
    tableBody.addEventListener("click", (e) => {
        if (!e.target.classList.contains("save-btn")) return;

        const row = e.target.closest(".pitch-row");
        savePitch(row);
    });
});

// 行テンプレート
function createRow() {
    return `
    <tr class="pitch-row">
        <td><input type="number" class="batter" placeholder="打者ID"></td>
        <td><input type="number" class="pitcher" placeholder="投手ID"></td>

        <td>
            <select class="batter_result">
                <option value="">--結果--</option>
                <option value="strikeout">三振</option>
                <option value="fly">フライ</option>
                <option value="groundout">ゴロアウト</option>
                <option value="lineout">ライナーアウト</option>
                <option value="double_play">併殺</option>
                <option value="single">単打</option>
                <option value="double">二塁打</option>
                <option value="triple">三塁打</option>
                <option value="homerun">本塁打</option>
                <option value="walk">四球</option>
                <option value="deadball">死球</option>
                <option value="error">エラー</option>
                <option value="fielder_choice">野選</option>
            </select>
        </td>

        <td>
            <select class="runner_action">
                <option value="">--走者--</option>
                <option value="none">なし</option>
                <option value="advance_1">1つ進塁</option>
                <option value="advance_2">2つ進塁</option>
                <option value="advance_3">3つ進塁</option>
                <option value="score">生還</option>
                <option value="out_on_base">走塁死</option>
            </select>
        </td>

        <td>
            <select class="pitch_result">
                <option value="">--投球--</option>
                <option value="ball">ボール</option>
                <option value="strike">ストライク</option>
                <option value="foul">ファウル</option>
                <option value="inplay">インプレー</option>
            </select>
        </td>

        <td>
            <button type="button" class="save-btn">保存</button>
        </td>
    </tr>`;
}

// 保存処理
function savePitch(row) {
    const gameId = document.querySelector("#game-id").value;

    const payload = {
        batter_id: row.querySelector(".batter").value,
        pitcher_id: row.querySelector(".pitcher").value,
        pitch_result: row.querySelector(".pitch_result").value,
        batter_result: row.querySelector(".batter_result").value,
        runner_action: row.querySelector(".runner_action").value,
    };

    fetch(`/games/${gameId}/score_input/save/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    })
        .then((res) => res.json())
        .then((data) => {
            if (!data.ok) {
                alert("保存エラー");
                return;
            }

            // 最新10件の表示更新
            updateRecentList(data.pitches);

            // 入力行をクリア
            clearRow(row);
        })
        .catch(() => alert("通信エラー"));
}

// 行クリア
function clearRow(row) {
    row.querySelector(".batter").value = "";
    row.querySelector(".pitcher").value = "";
    row.querySelector(".pitch_result").value = "";
    row.querySelector(".batter_result").value = "";
    row.querySelector(".runner_action").value = "";
}

// 最新10件を画面に反映
function updateRecentList(list) {
    const ul = document.querySelector("#recent-list");
    ul.innerHTML = "";

    list.forEach((p) => {
        const li = document.createElement("li");
        li.textContent = `${p.inning}回(${p.top_bottom}) 打者${p.batter_id} → ${p.batter_result}`;
        ul.appendChild(li);
    });
}
