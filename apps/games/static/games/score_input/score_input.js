// ------------------------------
// lineup_json の読み込み
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
// 現在の打者インデックス（1〜9をループ）
// ------------------------------
let batterIndex = 0;

// 現在の投球数
let pitchNumber = 1;

// 現在の回
let currentInning = 1;

// 表/裏（とりあえず表固定）
let isTopInning = true;


// ------------------------------
// 投手取得
// ------------------------------
function getPitcher(isTop) {
    const pitchingTeam = isTop ? lineup.bottom.pitching : lineup.top.pitching;
    const pitcher = pitchingTeam.find(p => p.position === "P");
    return pitcher || null;
}


// ------------------------------
// 打者取得
// ------------------------------
function getBatter(isTop) {
    const battingTeam = isTop ? lineup.top.batting : lineup.bottom.batting;

    console.log("battingTeam:", battingTeam);   // ★ デバッグ
    console.log("batterIndex:", batterIndex);

    const batter = battingTeam[batterIndex % battingTeam.length];
    batterIndex++;

    return batter;
}


// ------------------------------
// 行追加
// ------------------------------
function addRow() {
    const wrapper = document.createElement("tbody");
    wrapper.innerHTML = rowTemplate.trim();
    const row = wrapper.firstChild;

    // 打者
    const batter = getBatter(isTopInning);
    console.log("選択された打者:", batter);   // ★ デバッグ

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
// 保存処理
// ------------------------------
function savePitch(row) {
    const gameId = window.location.pathname.split("/")[2];

    const payload = {
        inning: currentInning,
        top_bottom: isTopInning ? "top" : "bottom",
        pitch_number: pitchNumber++,
        batting_order: Number(row.dataset.battingOrder),
        hitter_id: row.querySelector(".batter-id").value,
        pitch_result: row.querySelector(".pitch_result").value,
        atbat_result: row.querySelector(".batter_result").value || null,
    };

    console.log("送信payload:", payload); // ★ デバッグログ

    fetch(`/games/${gameId}/score_input/save/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify(payload),
    })
    .then(r => r.json())
    .then(data => {
        console.log("Saved:", data);
        row.querySelector(".save-btn").disabled = true;
        row.querySelector(".save-btn").textContent = "保存済";
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
// 行追加ボタン
// ------------------------------
addRowBtn.addEventListener("click", addRow);
