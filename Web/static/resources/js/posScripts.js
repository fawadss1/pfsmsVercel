const d = new Date();
let time = document.getElementById("time").innerHTML = d.getHours() + '' + d.getMinutes() + '' + d.getSeconds();

function printSlip(area) {
    if ($('#customerName').val() == "" && $('#selectedCustomer').val() == "") {
        alert('Please Enter Or Select The Customer Name First');
        $('#customerName').focus();
    } else {
        document.body.innerHTML = document.getElementById(area).outerHTML;
        window.print();
        location.reload();
    }
}

$('#customerName').keyup(function () {
    let name = $(this).val().replace(/^(.)|\s+(.)/g, c => c.toUpperCase());
    $('#cName').text(name);
    if ($(this).val().length > 0) {
        $("#selectedCustomer").attr("disabled", true);
    } else {
        $("#selectedCustomer").removeAttr("disabled");
    }
    JsBarcode("#barcode", name + " " + time, {
        format: "code128",
        lineColor: "black",
        background: "transparent",
        width: 2,
        height: 70,
        displayValue: false
    });
});
$('#selectedCustomer').change(function () {
    let name = $(this).val().replace(/^(.)|\s+(.)/g, c => c.toUpperCase());
    $('#cName').text(name);
    if ($(this).val() != "") {
        $("#customerName").attr("disabled", true);
    } else {
        $("#customerName").removeAttr("disabled");
    }
    JsBarcode("#barcode", name + " " + time, {
        format: "code128",
        lineColor: "black",
        background: "transparent",
        width: 2,
        height: 70,
        displayValue: false
    });
});
$('#fuelRs').keyup(function () {
    if ($(this).val().length > 0)
        $("#fuelltrs").attr("disabled", true);
    else
        $("#fuelltrs").removeAttr("disabled");
    let selectedFuel = $('#fuel').val();
    if (selectedFuel == "Petrol") {
        let ptrlPrice = $('.petrol_price').val();
        $('#petrol_price').text(ptrlPrice);
        let ltrs = $(this).val();
        let ptrlLtrsSold = ltrs / ptrlPrice;
        let ptrlSoldRs = ptrlPrice * ptrlLtrsSold;
        const ptrlInputVal = $('#ptrlSoldRsVal');
        ptrlInputVal.val(ptrlSoldRs);
        const totalRs = parseFloat(ptrlInputVal.val()) + parseFloat($('#dslSoldRsVal').val());
        $('#ptrlLtrSold').text(new Intl.NumberFormat('en-IN').format(ptrlLtrsSold));
        $('#ptrlSoldRs').text(new Intl.NumberFormat('en-IN').format(ptrlSoldRs));
        $('#totalRs').text(new Intl.NumberFormat('en-IN').format(totalRs));

    } else if (selectedFuel == "Diesel") {
        let dieselPrice = $('.diesel_price').val();
        $('#diesel_price').text(dieselPrice);
        let ltrs = $(this).val();
        let dslLtrsSold = ltrs / dieselPrice;
        let dslSoldRs = dieselPrice * dslLtrsSold;
        const dslInputValue = $('#dslSoldRsVal');
        dslInputValue.val(dslSoldRs);
        const totalRs = parseFloat($('#ptrlSoldRsVal').val()) + parseFloat(dslInputValue.val());
        $('#dslLtrSold').text(new Intl.NumberFormat('en-IN').format(dslLtrsSold));
        $('#dslSoldRs').text(new Intl.NumberFormat('en-IN').format(dslSoldRs));
        $('#totalRs').text(new Intl.NumberFormat('en-IN').format(totalRs));
    } else {
        alert('Please Select Fuel First');
        $('#fuelRs').val('');
    }
});

$('#fuelltrs').keyup(function () {
    if ($(this).val().length > 0)
        $("#fuelRs").attr("disabled", true);
    else
        $("#fuelRs").removeAttr("disabled");
    let selectedFuel = $('#fuel').val();
    if (selectedFuel == "Petrol") {
        let ptrlPrice = $('.petrol_price').val();
        $('#petrol_price').text(ptrlPrice);
        let ltrs = $(this).val();
        let ptrlSoldRs = ptrlPrice * ltrs;
        const ptrlInputVal = $('#ptrlSoldRsVal');
        ptrlInputVal.val(ptrlSoldRs);
        const totalRs = parseFloat(ptrlInputVal.val()) + parseFloat($('#dslSoldRsVal').val());
        $('#ptrlLtrSold').text(ltrs);
        $('#ptrlSoldRs').text(new Intl.NumberFormat('en-IN').format(ptrlSoldRs));
        $('#totalRs').text(new Intl.NumberFormat('en-IN').format(totalRs));
    } else if (selectedFuel == "Diesel") {
        let dieselPrice = $('.diesel_price').val();
        $('#diesel_price').text(dieselPrice);
        let ltrs = $(this).val();
        let dslSoldRs = dieselPrice * ltrs;
        const dslInputValue = $('#dslSoldRsVal');
        dslInputValue.val(dslSoldRs);
        const totalRs = parseFloat($('#ptrlSoldRsVal').val()) + parseFloat(dslInputValue.val());
        $('#dslLtrSold').text(ltrs);
        $('#dslSoldRs').text(new Intl.NumberFormat('en-IN').format(dslSoldRs));
        $('#totalRs').text(new Intl.NumberFormat('en-IN').format(totalRs));
    } else {
        alert('Please Select Fuel First');
        $('#fuelltrs').val('');
    }
});
$('#fuel').change(function () {
    $('#fuelRs').val(null);
    $('#fuelltrs').val(null);
});
