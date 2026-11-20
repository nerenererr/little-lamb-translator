
import { pipeline } from 'https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.0.2';


const trButton = document.getElementById('trButton');
const switchButton = document.getElementById('switchButton');
const inputText = document.getElementById('inputText');
const status = document.getElementById('status');
const result = document.getElementById('result');


let translator = null;
let direction = 'en-es';
let loadedDirection = null;


const models = {
    'en-es': 'Xenova/opus-mt-en-es',
    'es-en': 'Xenova/opus-mt-es-en'
};


async function init() {
    status.innerText = 'Loading model...';

    const model = models[direction];
    const supportsGpu = 'gpu' in navigator;

    if (supportsGpu) {
        try {
            translator = await pipeline('translation', model, {
                device: 'webgpu'
            });

            loadedDirection = direction;
            status.innerText = 'Model loaded (WebGPU)';
            return;

        } catch (error) {
            console.warn('WebGPU failed, trying WASM...', error);
            status.innerText = 'Trying WASM...';
        }
    }

    translator = await pipeline('translation', model, {
        device: 'wasm'
    });

    loadedDirection = direction;
    status.innerText = 'Model loaded (WASM)';
}

async function translate() {
    const text = inputText.value.trim();

    if (!text) {
        status.innerText = 'Please write something first!';
        return;
    }

    trButton.disabled = true;
    switchButton.disabled = true;

    try {
        if (translator === null || loadedDirection !== direction) {
            await init();
        }

        status.innerText = 'Translating...';

        const output = await translator(text);

        result.innerText = output[0].translation_text;
        status.innerText = 'Done!';

    } catch (error) {
        console.error('Translation error:', error);
        status.innerText = 'Something went wrong!';
        translator = null;
        loadedDirection = null;

    } finally {
        trButton.disabled = false;
        switchButton.disabled = false;
    }
}

function switchLanguage() {
    direction = direction === 'en-es' ? 'es-en' : 'en-es';

    translator = null;
    loadedDirection = null;
    result.innerText = '';

    switchButton.innerText = direction === 'en-es'
        ? 'English → Spanish'
        : 'Spanish → English';

    inputText.placeholder = direction === 'en-es'
        ? 'Write something in English...'
        : 'Escribe algo en español...';

    status.innerText = 'Ready to translate!';
}

trButton.addEventListener('click', translate);
switchButton.addEventListener('click', switchLanguage);
