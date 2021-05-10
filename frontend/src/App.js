import './App.css';
import Homepage from './pages/homepage.component';
import Header from './components/header/header.component';
import { Switch, Route } from 'react-router-dom';

function App() {
  console.log(typeof(Header));
  return (
    <div>
      <Header />
      <Switch>
        <Route path="/" component={Homepage} exact />
      </Switch>
    </div>
  );
}

export default App;
