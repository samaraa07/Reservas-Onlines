// Abre e fecha o dropdown
document.getElementById("serviceSelect").addEventListener("click", function () {
  const menu = document.getElementById("dropdownMenu");
  menu.style.display = menu.style.display === "block" ? "none" : "block";
});

// Fecha ao clicar fora
document.addEventListener("click", function (event) {
  const container = document.querySelector(".custom-select-container");
  if (!container.contains(event.target)) {
    document.getElementById("dropdownMenu").style.display = "none";
  }
});

// Seleciona item final
document.querySelectorAll(".submenu li, .dropdown > ul > li:not(.has-submenu)").forEach(item => {
  item.addEventListener("click", function () {
    const value = this.getAttribute("data-value");
    document.getElementById("serviceInput").value = value;
    document.getElementById("serviceSelect").innerText = value;
    document.getElementById("dropdownMenu").style.display = "none";
  });
});
