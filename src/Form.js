import {useState} from 'react'
function Form() {
    const [form, setForm] = useState({
        job: "",
        degree: "",
        experience: ""
    })
    const handleSubmit = (event) => {
        event.preventDefault()

        const form_data = new FormData
        form_data.append("1", form.job)
        form_data.append("2", form.degree)
        form_data.append("3", form.experience)

        fetch('http://127.0.0.1:5000', {
            method: 'POST',
            body: form_data
        })
            .then(response => console.log(response))
    }

    const onChange = (event) => {
        console.log("Changed input field")
        const name = event.target.name
        const value = event.target.value
        setForm({...form, [name]: value})
    }

    return (
        <form onSubmit={handleSubmit}>
            <h4>Salary Prediction Model</h4>
            <p>Example to predict tech career salaries</p>
            <input type="text" name="job" onChange={onChange} placeholder="Job Title"/>
            <input type="text" name="degree" onChange={onChange} placeholder="Highest Degree"/>
            <input type="number" name="experience" onChange={onChange} placeholder="Years of Experience"/>
            <button type="submit">Submit Form</button>
        </form>
    )
}
export default Form