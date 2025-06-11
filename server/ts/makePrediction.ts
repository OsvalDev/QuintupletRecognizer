const pathsPresets = {
    itsuki: 'static/img/itsukiPreset.jpeg',
    yotsuba: 'static/img/yotsubaPreset.jpeg',
    miku: 'static/img/mikuPreset.jpeg',
    nino: 'static/img/ninoPreset.jpeg',
    ichika: 'static/img/ichikaPreset.jpeg'
}
const pathsResults = {
    itsuki: 'static/img/itsukiDefault.webp',
    yotsuba: 'static/img/yotsubaDefault.webp',
    miku: 'static/img/mikuDefault.webp',
    nino: 'static/img/ninoDefault.webp',
    ichika: 'static/img/ichikaDefault.webp',
    asuna: 'static/img/asunaDefault.jpg',
    chizuru: 'static/img/chizuruDefault.jpg',
    zerotwo: 'static/img/zerotwoDefault.png',
    kaede: 'static/img/kaedeDefault.jpg',
    mai: 'static/img/maiDefault.jpg',
    mami: 'static/img/mamiDefault.jpg',
    rei: 'static/img/reiDefault.jpg',
    ruka: 'static/img/rukaDefault.jpg',
    serena: 'static/img/serenaDefault.jpg',
    sumi: 'static/img/sumiDefault.webp'
}

const requirePredictionPreset = async (path : string) => {
    try {
        showCurrentImg(path);
        const response = await fetch(`http://${window.location.hostname}:5000/submitPreset`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                pathPreset: path
            })
        });

        if (response.ok) {
            const data = await response.json();
            showResults(data.confidence, data.name);
        } else {
            console.error('Error in response:', response.statusText);
        }
    } catch (error) {
        console.error('Request failed', error);
    }
};

const requirePrediction = async (e : SubmitEvent) => {
    e.preventDefault();
    try {
        const fileInput = document.getElementById('file-input') as HTMLInputElement;

        if (fileInput && fileInput.files && fileInput.files[0]) {
            const imageFile = fileInput.files[0];    
            const formData = new FormData();
            formData.append('my_image', imageFile);
    
            const response = await fetch(`http://${window.location.hostname}:5000/submit`, {
                method: 'POST',
                body: formData
            });
    
            if (response.ok) {
                const data = await response.json();
                showResults(data.confidence, data.name);
                showCurrentImg(data.img_path);
            } else {
                console.error('Error in response:', response.statusText);
            }
        } else {
            console.error("No image selected");
            return;
        }
    } catch (error) {
        console.error('Request failed', error);
    }
};

const showResults = (confidence: number, sister: string) => {
    const bodyContainer = document.getElementById('body-container') as HTMLElement;

    if (bodyContainer.lastChild) bodyContainer.removeChild(bodyContainer.lastChild);

    const id = sister as keyof typeof pathsResults ;
    const imgPath = pathsResults[id];

    const div = document.createElement('div');
    div.classList.add('fixed', 'top-0', 'right-12', 'w-fit', 'h-full', 'p-4', 'flex', 'items-center', 'justify-center', 'fade-in')

    const img = document.createElement('img') as HTMLImageElement;
    img.src = imgPath;
    img.classList.add('w-60');

    const divContainer = document.createElement('div');
    
    const nameSisterElement = document.createElement('p');
    nameSisterElement.textContent = sister;
    nameSisterElement.classList.add('text-5xl', 'font-bold', 'text-secondary');

    const confidenceElement = document.createElement('p');
    confidenceElement.classList.add('text-lg', 'mt-2');
    confidenceElement.textContent = (Math.floor(confidence * 100)).toString() + '%';

    divContainer.appendChild(nameSisterElement);
    divContainer.appendChild(confidenceElement);

    div.appendChild(img);
    div.appendChild(divContainer);

    bodyContainer.appendChild(div);

    setTimeout(() => {
        div.classList.add('show');
    }, 10);
};

const showCurrentImg = (imgPath : string) => {
    const imgElement = document.getElementById('previewImg') as HTMLImageElement || null;
    if (imgElement) {
        imgElement.src = `${imgPath}?t=${new Date().getTime()}`;
    } else {
        const div = document.createElement('div');
        div.classList.add('flex', 'flex-col', 'mt-4');
        const p = document.createElement('p');
        p.textContent = 'Image preview';
        p.classList.add('font-semibold', 'w-full', 'text-center')
        const img = document.createElement('img');
        img.src = `${imgPath}?t=${new Date().getTime()}`;
        img.id = 'previewImg';
        img.classList.add('h-60', 'mt-4');

        div.appendChild(p);
        div.appendChild(img);
        const container = document.querySelector('main') as HTMLElement;
        container.appendChild(div);
    }
};

const initializeEvents = () => {
    const presetElements = document.querySelectorAll('.preset');
    presetElements.forEach((element) => {
        const id = element.id as keyof typeof pathsPresets ;
        element.addEventListener("click", () => requirePredictionPreset(pathsPresets[id]));
    })

    const form = document.getElementById('my-form') as HTMLElement;
    form.addEventListener('submit', requirePrediction);
};

initializeEvents();
