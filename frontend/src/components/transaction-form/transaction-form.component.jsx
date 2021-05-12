import React from 'react';
import FormInput from '../form-input/form-input.component';
import SubmitButton from '../submit-button/submit-button.component';

import axios from 'axios';

class TransactionForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            transactionDate: '',
            shareAmount: 1,
            sharePrice: 0.0,
            shareTicker: ''
        }
    }

    handleChange = event => {
        const {name, value} = event.target;
        this.setState({
            [name]: value
        });
    }

    handleSubmit = event => {
        event.preventDefault();
        const {transactionDate, shareAmount, sharePrice, shareTicker } = this.state,
            transactionAmount = (sharePrice*shareAmount).toFixed(4);
        console.log(transactionAmount);
        const transactionInfo = {
            investor: 1,
            transaction_date: transactionDate,
            amount: transactionAmount,
            assent_name: shareTicker
        };
        
        axios.post('http://localhost:8000/api/transactions/', transactionInfo)
            .then(response => console.log(response))
            .catch(error => console.log(error));    
    }

    render() {
        return (
            <form>
                <FormInput label="Ticker" name="shareTicker" value={this.state.shareTicekr} type="text" handleChange={this.handleChange} />
                <FormInput label="Transaction Date" name="transactionDate" type="date" value={this.state.transactionDate} handleChange={this.handleChange} />
                <FormInput label="Share Price" name="sharePrice" type="number" value={this.state.sharePrice} handleChange={this.handleChange} min="0" step="0.01" />
                <FormInput label="Amount" name="shareAmount" type="number" value={this.state.shareAmount} handleChange={this.handleChange} min="1" />
                <SubmitButton submit={this.handleSubmit}>Add Transaction</SubmitButton>
            </form>
        )
    }
}

export default TransactionForm;