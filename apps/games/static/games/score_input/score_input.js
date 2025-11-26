// ------------------------------
// lineup_json
// ------------------------------
const lineupDataTag = document.getElementById("lineup-data");
const lineup = JSON.parse(lineupDataTag.textContent);

// ------------------------------
// DOM
// ------------------------------
const addRowBtn = document.getElementById("add-row-btn");
const pitchBody = document.getElementById("pitch-body");
const rowTemplate = document.getElementById("row-template").innerHTML;

// ------------------------------
// 進行状態
// ------------------------------
let batterIndex = 0;
let pitchNumber = 1;
let currentInning = 1;
let isTopInning = true;

// ------------------------------
// 投手
// ------------------------------
function getPitcher(isTop) {
    const pitchingTeam = isTop ? lineup.bottom.pitching : lineup.top.pitching;
    return pitchingTeam.find(p => p.position === "P") || null;
}

// ------------------------------
// 打者
// ------------------------------
function getBatter(isTop) {
    const battingTeam = isTop ? lineup.top.batting : lineup.bottom.batting;
    const batter = battingTeam[batterIndex % battingTeam.length];
    batterIndex++;
    return batter;
}

// ------------------------------
// 新規行
// ------------------------------
function addRow() {
    console.log("addRow 呼ばれたよ");
    
    const wrapper = document.createElement("tbody");
    wrapper.innerHTML = rowTemplate.trim();
    const row = wrapper.firstChild;

    // 打者
    const batter = getBatter(isTopInning);
    row.querySelector(".batter-name").textContent = batter.name;
    row.querySelector(".batter-id").value = batter.id;
    row.dataset.battingOrder = batter.order;

    // 投手
    const pitcher = getPitcher(isTopInning);
    if (pitcher) {
        row.querySelector(".pitcher-name").textContent = pitcher.name;
        row.querySelector(".pitcher-id").value = pitcher.id;
    }

    // 保存ボタン
    const saveBtn = row.querySelector(".save-btn");
    saveBtn.addEventListener("click", () => savePitch(row));

    pitchBody.appendChild(row);
}

// ------------------------------
// 保存
// ------------------------------
function savePitch(row) {
    const gameId = window.location.pathname.split("/")[2];

    const payload = {
        game_id: Number(gameId),
        inning: currentInning,
        top_bottom: isTopInning ? "top" : "bottom",
        pitch_number: pitchNumber++,
        batting_order: Number(row.dataset.battingOrder),
        hitter_id: row.querySelector(".batter-id").value,
        pitch_result: row.querySelector(".pitch_result").value,
        atbat_result: row.querySelector(".batter_result").value || null,
        runner_action: row.querySelector(".runner_action").value || null,  // ★追加
    };

    fetch(`/games/api/pitch/save/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify(payload),
    })
    .then(r => r.json())
    .then(data => {
        const saveBtn = row.querySelector(".save-btn");
        saveBtn.disabled = true;
        saveBtn.textContent = "保存済";
    })
    .catch(err => console.error(err));
}

// ------------------------------
// CSRF
// ------------------------------
function getCSRFToken() {
    const name = "csrftoken=";
    const decoded = decodeURIComponent(document.cookie);
    const parts = decoded.split(";");
    for (let p of parts) {
        p = p.trim();
        if (p.startsWith(name)) return p.substring(name.length);
    }
    return "";
}

// ------------------------------
// 既存投球の描画
// ------------------------------
function renderExistingRow(p) {
    const wrapper = document.createElement("tbody");
    wrapper.innerHTML = rowTemplate.trim();
    const row = wrapper.firstChild;

    row.querySelector(".batter-name").textContent = p.batter_name;
    row.querySelector(".batter-id").value = p.batter_id;
    row.dataset.battingOrder = p.batting_order;

    row.querySelector(".pitcher-name").textContent = p.pitcher_name;
    row.querySelector(".pitcher-id").value = p.pitcher_id;

    row.querySelector(".pitch_result").value = p.pitch_result ?? "";
    row.querySelector(".batter_result").value = p.atbat_result ?? "";
    row.querySelector(".runner_action").value = p.runner_action ?? "";  // ★追加

    const saveBtn = row.querySelector(".save-btn");
    saveBtn.disabled = true;
    saveBtn.textContent = "保存済";

    pitchBody.appendChild(row);
}

// ------------------------------
// ページロード
// ------------------------------
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOMContentLoaded 発火したよ");

    const existingTag = document.getElementById("existing-pitches");
    const existingPitches = JSON.parse(existingTag.textContent);

    console.log("existingPitches =", existingPitches);

    existingPitches.forEach(p => {
        console.log("描画 row:", p);
        renderExistingRow(p);
    });

    if (existingPitches.length > 0) {
        pitchNumber = existingPitches[existingPitches.length - 1].pitch_number + 1;
    }

    console.log("pitchNumber after load =", pitchNumber);

    addRowBtn.addEventListener("click", () => {
        console.log("ボタン押された！");
        addRow();
    });
});
