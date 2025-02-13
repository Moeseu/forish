document.addEventListener("DOMContentLoaded", function () {
    // Видалення товару з кошика
    document.querySelectorAll(".remove-from-cart").forEach(button => {
        button.addEventListener("click", function () {
            const gameId = this.getAttribute("data-game-id");

            fetch(`/remove_from_cart/${gameId}`, { method: "POST" })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById(`cart-item-${gameId}`).remove();
                        updateTotalPrice();
                    } else {
                        alert("Error removing item: " + data.error);
                    }
                });
        });
    });

    // Оформлення замовлення
    document.getElementById("checkout-button")?.addEventListener("click", function () {
        fetch("/checkout", { method: "POST" })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Order placed successfully!");
                    location.reload();
                } else {
                    alert("Error processing order: " + data.error);
                }
            });
    });

    // Оновлення загальної ціни після видалення товару
    function updateTotalPrice() {
        let total = 0;
        document.querySelectorAll(".card-text.fw-bold.text-primary").forEach(priceTag => {
            total += parseFloat(priceTag.textContent.replace("$", ""));
        });
        document.querySelector(".total-price").textContent = `$${total.toFixed(2)}`;
    }
});
