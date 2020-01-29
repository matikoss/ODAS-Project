const calculatePasswordEntropy = (password) => {
    const pool = 86;
    const length = password.length;
    return Math.log2(Math.pow(pool, length))
};

const changeEntropyOutput = (entropy) => {
    const entropyText = $("#new-password-entropy-result");
    entropyText.text(`Password entropy: ${entropy}`);
    console.log(entropy);
    console.log(entropyText)
};