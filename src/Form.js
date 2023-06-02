import {useState} from 'react'
import Select from 'react-select'
import "./Form.css"
function Form() {
    const [form, setForm] = useState({
        job: "",
        degree: "",
        experience: ""
    })
    const jobs = [
      "Business Analyst",
      "Data Scientist",
      "Hardware Engineer",
      "Human Resources",
      "Management Consultant",
      "Marketing",
      "Mechanical Engineer",
      "Product Designer",
      "Product Manager",
      "Recruiter",
      "Sales",
      "Software Engineer",
      "Software Engineering Manager",
      "Solution Architect",
      "Technical Program Manager"
    ];
    const degrees = [
        {value: "1", label: "Bachelor's Degree"},
        {value: "2", label: "Master's Degree"},
        {value: "3", label: "Doctorate (PhD)"},
    ];

    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState("")

    const [receivedText, setReceivedText] = useState('');
    const handleSubmit = async (event) => {
        event.preventDefault()
        console.log("Form Submitted")
        console.log(form)

        const form_data = new FormData
        form_data.append("1", form.job)
        form_data.append("2", form.degree)
        form_data.append("3", form.experience)

        setLoading(true)

        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            mode: 'cors',
            body: form_data,
        })
        .then(response => response.text())
        .then(html => {
            setResult(html)
            setLoading(false)
        })
    }
    const onChange = (event) => {
        console.log("Changed input field")
        const name = event.target.name
        const value = event.target.value
        setForm({...form, [name]: value})
    }

    const handleClear = () => {
        setForm({
            job: "",
            degree: "",
            experience: 0
        })
        setResult("")
    }
    const jobChange = (selectedOption, name) => {
        console.log("jobChange", selectedOption);
        setForm({ ...form, ["job"]: selectedOption.value });
    }
    const degreeChange = (selectedOption, name) => {
        console.log("degreeChange", selectedOption);
        setForm({ ...form, ["degree"]: selectedOption.value });
    }
    const [sliderValue, setSliderValue] = useState(0);

    const handleSliderChange = (event) => {
        setSliderValue(parseInt(event.target.value));
        setForm({ ...form, ["experience"]: event.target.value })
    };

    return (
        <form onSubmit={handleSubmit}>
            <h4>Salary Prediction Model</h4>
            <p>Example to predict tech career salaries</p>

            <Select options={jobs.map(option => ({ value: option, label: option }))} onChange={jobChange} placeholder={"Job Title"}/>
            <Select options={degrees} onChange={degreeChange} placeholder={"Degree"}/>

            <p>Years of Experience: {sliderValue}</p>
            <input type="range" min={0} max={20} value={sliderValue} onChange={handleSliderChange}

            />

            <button type="submit" disabled={loading}>Submit Form</button>

            {result && <span onClick={handleClear}>Clear Prediction</span> }
            {result && <div dangerouslySetInnerHTML={{__html: result}} className="result"/> }
        </form>

    )
}
export default Form