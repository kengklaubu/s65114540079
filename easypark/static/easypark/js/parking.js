function fetchParkingStatus() {
    $.ajax({
        url: "{% url 'get_parking_status' %}",
        method: "GET",
        success: function (data) {
            console.log(data);  // เพิ่มบรรทัดนี้เพื่อตรวจสอบข้อมูลที่ได้รับ
            data.forEach(function (spot) {
                var spotElement = document.getElementById("spot-" + spot.spot_number);
                if (spot.is_available) {
                    spotElement.style.backgroundColor = "green";  // ช่องว่าง
                } else {
                    spotElement.style.backgroundColor = "red";    // ช่องไม่ว่าง
                }
            });
        }
    });
}

function showSpotDetails(spotNumber) {
    $.ajax({
        url: "{% url 'get_spot_details' %}?spot=" + spotNumber,
        method: "GET",
        success: function(data) {
            document.getElementById("details-container").innerHTML = `
                <h3>ช่องจอดหมายเลข ${data.spot_number}</h3>
                <p>${data.details}</p>
            `;
        }
    });
}





// ดึงสถานะที่จอดทุกๆ 5 วินาที
setInterval(fetchParkingStatus, 5000);
