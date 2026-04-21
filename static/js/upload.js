function loadSemesters() {

    let course = document.getElementById("course").value.toLowerCase(); // ✅ FIX
    let semester = document.getElementById("semester");

    semester.innerHTML = "<option value=''>Select Semester</option>";

    if (course !== "") {
        for (let i = 1; i <= 6; i++) {
            let opt = document.createElement("option");
            opt.text = "Semester " + i;
            opt.value = i;
            semester.appendChild(opt);
        }
    }

    document.getElementById("subject").innerHTML = "<option value=''>Select Subject</option>";
}



function loadSubjects() {

    let course = document.getElementById("course").value.toLowerCase(); // ✅ FIX
    let semester = document.getElementById("semester").value;
    let subject = document.getElementById("subject");

    subject.innerHTML = "<option value=''>Select Subject</option>";

    let subjects = {

        mca: {
            1: ["Programming in C", "Mathematics", "Computer Fundamentals"],
            2: ["Data Structures", "Operating System", "DBMS"],
            3: ["Java Programming", "Computer Networks", "Software Engineering"],
            4: ["Machine Learning", "Cloud Computing", "AI"],
            5: ["Cyber Security", "Big Data", "IoT"],
            6: ["Project Work"]
        },

        bsc: {
            1: ["Physics", "Chemistry", "Mathematics"],
            2: ["Statistics", "Computer Science", "Electronics"],
            3: ["Data Analysis", "Numerical Methods", "Algorithms"],
            4: ["DBMS", "Operating System", "Java"],
            5: ["AI", "Machine Learning"],
            6: ["Project"]
        },

        bba: {
            1: ["Business Communication", "Principles of Management"],
            2: ["Marketing Management", "Financial Accounting"],
            3: ["Human Resource Management", "Business Law"]
        },

        mba: {
            1: ["Management Principles", "Business Economics"],
            2: ["Marketing Strategy", "Financial Management"],
            3: ["Business Analytics", "Corporate Strategy"]
        },

        msc: {
            1: ["Advanced Mathematics", "Research Methodology"],
            2: ["Artificial Intelligence", "Data Analytics"],
            3: ["Deep Learning", "Big Data"]
        }

    };

    if (subjects[course] && subjects[course][semester]) {

        subjects[course][semester].forEach(function (sub) {

            let opt = document.createElement("option");
            opt.text = sub;
            opt.value = sub;
            subject.appendChild(opt);

        });

    }

}


// ✅ FILE NAME SHOW FIX (SAFE)
document.addEventListener("DOMContentLoaded", function () {

    let fileInput = document.getElementById("fileUpload");
    let fileName = document.getElementById("fileName");

    if (fileInput) {
        fileInput.addEventListener("change", function () {
            if (this.files.length > 0) {
                fileName.innerText = this.files[0].name;
            }
        });
    }

});