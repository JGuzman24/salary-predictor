import {useState} from 'react'
import Select from 'react-select'
import "./Form.css"
function Form() {
    const [form, setForm] = useState({
        job: "",
        degree: "",
        experience: ""
    })
    const options = [
        {value: "Software Engineer", label: "Software Engineer"},
        {value: "Sales", label: "Sales"},
        {value: "Data Scientist", label: "Data Scientist"},
    ]

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

    const [selectedOption, setSelectedOption] = useState('')
    const handleOptionChange = (event) => {
        setSelectedOption(event.target.value);
    }


    const handleClear = () => {
        setForm({
            job: "",
            degree: "",
            experience: 0
        })
        setResult("")
    }
    const handleChange = (selectedOption) => {
        console.log("handleChange", selectedOption)
        const name = selectedOption.target.name
        const value = selectedOption.target.value
        setForm({...form, [name]: value})
    }

    return (
        <form onSubmit={handleSubmit}>
            <h4>Salary Prediction Model</h4>
            <p>Example to predict tech career salaries</p>

            <input type="text" name="job" value={form.job} onChange={onChange} placeholder="Job Title" required />
            <input type="text" name="degree"value={form.degree} onChange={onChange} placeholder="Highest Degree" required />
            <input type="number" name="experience" value={form.experience} onChange={onChange} placeholder="Years of Experience" required />
            <button type="submit" disabled={loading}>Submit Form</button>

            {result && <span onClick={handleClear}>Clear Prediction</span> }
            {result && <div dangerouslySetInnerHTML={{__html: result}} className="result"/> }

            <Select options={options} onChange={handleChange} label="job" />
            <select value={selectedOption} onChange={handleOptionChange}>
                <option value="">Degree</option>
                <option value="Bachelors">Bachelors</option>
                <option value="Masters">Masters</option>
                <option value="PhD">PhD</option>
            </select>

        </form>
    )
}
export default Form