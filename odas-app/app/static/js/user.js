const calculatePasswordEntropy = (password) => {
    const pool = 86;
    const length = password.length;
    return Math.log2(Math.pow(pool, length))
};

const changeEntropyOutput = (entropy) => {
    const entropyText = $("#new-password-entropy-result");
    entropyText.text(`Password entropy: ${entropy}`);
    const qualityText = $("#new-pass-quality-field");
    qualityText.text(`Strength: ${calculateQuality(entropy)}`);
};

const calculateQuality = (entropy) => {
    let result;
    if (entropy < 28) {
        result = "Very Weak"
    } else if (entropy >= 28 && entropy <= 35) {
        result = "Weak"
    } else if (entropy >= 35 && entropy <= 59) {
        result = "Reasonable"
    } else if (entropy >= 60 && entropy <= 127) {
        result = "Strong"
    } else if (entropy >= 128) {
        result = "Very Strong"
    }
    return result
};