function increase(){
    let insert = document.querySelector('.fertilizer_space');
    insert.innerHTML += 
    `<div class="col-5 fertilizer_space_insert">
        <label for="fertilizer" class="form-label">肥料</label>
        <select id="fertilizer" name='information_fertilizer' class="form-select is-invalid" required>
            <option selected disabled value="">選擇肥料...</option>
            <option value="urea">尿素</option>
            <option value="superphosphate">過磷酸鈣</option>
            <option value="potassium_chloride">氯化鉀</option>
            <option value="calcium_ammonium_nitrate">硝酸銨鈣(肥料用)</option>
        </select>
    </div>
    <div class="col-5 fertilizer_space_insert">
        <label for="dosage_fertilizer" class="form-label">肥料用量(單位kg)</label>
        <input type="text" name='information_dosage_fertilizer' class="form-control" id="dosage_fertilizer" value="" required>
        <div class="invalid-feedback">
            請填寫肥料用量
        </div>
    </div>`;
    let h = document.querySelector(".bodyMask"),vh = 0;
    vh = parseInt(h.style.height.substring(0, h.style.height.length -2)) + 13;
    console.log(vh);
    h.style.height = `${vh}vh`;
}

function reduce(){
    try{
        let _ = document.getElementsByClassName('fertilizer_space_insert');
        let _foo = _[_.length - 1];
        let _bar = _[_.length - 2];
        _foo.remove();
        _bar.remove();
        let h = document.querySelector(".bodyMask"),vh = 0;
        vh = parseInt(h.style.height.substring(0, h.style.height.length -2)) - 13;
        console.log(vh);
        h.style.height = `${vh}vh`;
    }catch(error){
        console.log(`ERROR: ${error}`)
    }
}