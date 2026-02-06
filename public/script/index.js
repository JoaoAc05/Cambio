async function runBot() {
    document.getElementById("result").innerText = "Executando...";
    const res = await fetch("/api/index");
    const data = await res.json();
    document.getElementById("result").innerText = JSON.stringify(data, null, 2);
}