function increase(){
    let insert = document.querySelector('.fertilizer_space');
    insert.innerHTML += 
    `<div class="col-5 fertilizer_space_insert">
        <label for="fertilizer" class="form-label">肥料</label>
        <select id="fertilizer" name='information' class="form-select is-invalid" required>
            <option selected disabled value="">選擇肥料...</option>
            <!-- <option value="Compound_Fertilizer_No.1">1號複合肥料</option>
                <option value="Compound_Fertilizer_No.4">4號複合肥料</option>
                <option value="Compound_Fertilizer_No.5">5號複合肥料</option>
                <option value="Compound_Fertilizer_No.25">25號複合肥料</option>
                <option value="Compound_Fertilizer_No.36">36號複合肥料</option>
                <option value="Compound_Fertilizer_No.39">39號複合肥料</option>
                <option value="Compound_Fertilizer_No.42">42號複合肥料</option>
                <option value="Compound_Fertilizer_No.43">43號複合肥料</option>
                <option value="ammonium_sulfate">硫酸銨</option> -->
            <option value="urea">尿素</option>
            <option value="superphosphate">過磷酸鈣</option>
            <option value="potassium_chloride">氯化鉀</option>
            <option value="calcium_ammonium_nitrate">硝酸銨鈣(肥料用)</option>
        </select>
    </div>
    <div class="col-5 fertilizer_space_insert">
        <label for="dosage_fertilizer" class="form-label">肥料劑量</label>
        <input type="text" name='information' class="form-control" id="dosage_fertilizer" value="" required>
        <div class="invalid-feedback">
            請填寫肥料劑量
        </div>
    </div>`;
}

function reduce(){
    try{
        let _ = document.getElementsByClassName('fertilizer_space_insert');
        let _foo = _[_.length - 1];
        let _bar = _[_.length - 2];
        _foo.remove();
        _bar.remove();
    }catch(error){
        console.log(`ERROR: ${error}`)
    }
}