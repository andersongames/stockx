function handleSharesNumber(targetId, increment) {
    // Get the current value of the shares input element
    const sharesInput = document.getElementById(targetId);
    let shares = parseInt(sharesInput.value);

    if (shares < 0 || isNaN(shares)) {
        // Prevent negative value
        sharesInput.value = "";

        return shares;
    }

    if (increment !== undefined) {
        // Calculate the new value based on the increment parameter
        if (increment) {
            shares += 1;
        } else {
            // Check if decrementing would result in a negative value, and prevent it
            if (shares > 0) {
                shares -= 1;
            }
        }

        // Update the input element with the new value
        sharesInput.value = shares;
    }

    return shares;
}

function updateTable(symbol, increment) {
    // Update the input element with the new value
    const shares = handleSharesNumber(`${symbol}-shares`, increment)

    if (isNaN(shares)) {
        // Do nothing if shares is empty
        return;
    }

    // Update variation element
    const variationContainerElem = document.getElementById(`variation-container-${symbol}`);
    const variationPrefixElem = document.getElementById(`variation-prefix-${symbol}`);
    const variationElem = document.getElementById(`variation-${symbol}`);
    const sharesElem = document.getElementById(`${symbol}-shares`);
    const originalShares = parseInt(sharesElem.getAttribute("data-shares"));
    const variation = shares - originalShares;
    variationElem.textContent = variation;
    if (variation > 0) {
        variationPrefixElem.textContent = "+";
        variationContainerElem.classList.add("text-success");
        variationContainerElem.classList.remove("text-danger");
    } else if (variation < 0) {
        variationPrefixElem.textContent = "";
        variationContainerElem.classList.remove("text-success");
        variationContainerElem.classList.add("text-danger");
    } else {
        variationPrefixElem.textContent = "";
        variationContainerElem.classList.remove("text-success");
        variationContainerElem.classList.remove("text-danger");
    }

    // Get the price of the share
    const sharePrice = document.getElementById(`${symbol}-price`);
    const priceValue = parseFloat(sharePrice.textContent);

    // Get total
    const totalElem = document.getElementById("total");
    let total = parseFloat(totalElem.textContent);

    // Calculate new total values
    let sharesTotalElem = document.getElementById(`${symbol}-total`);
    let sharesTotal = parseFloat(sharesTotalElem.textContent);
    const newSharesTotal = priceValue * shares;
    total = (total - sharesTotal) + newSharesTotal;

    // Update shares total
    sharesTotalElem.textContent = newSharesTotal.toFixed(2);

    // Update weight
    const inputs = document.querySelectorAll(".shares-input");
    for (let i = 0; i < inputs.length; i++) {
        // Get symbol
        const inputElem = document.getElementById(inputs[i].id);
        const symb = inputElem.getAttribute("data-symbol");

        // Get total shares
        sharesTotalElem = document.getElementById(`${symb}-total`);
        sharesTotal = parseFloat(sharesTotalElem.textContent);

        // Update weight
        const weightElem = document.getElementById(`${symb}-weight`);
        const newWeight = total === 0 ? 0 : sharesTotal / total * 100;
        weightElem.textContent = newWeight.toFixed(2);
    }

    // Update the total element with the new value
    totalElem.textContent = total.toFixed(2);
}
