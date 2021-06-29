import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Button, Icon, Input, Label, Menu } from 'semantic-ui-react';
import { findPeople, findPeopleStatus } from '../redux/actions/peopleActions';

const Header = () => {
    let [query, setQuery] = useState('');
    const dispatch = useDispatch();
    const people = useSelector((state) => state.people);
    
    // Poll status
    useEffect(() => {
        const timer = setInterval(() => axios
            .get('http://localhost:5000/api/v1/scraper/google/findpeople/status')
            .then((response) => {
                debugger;
                dispatch(findPeopleStatus(response.data));
            })
            .catch((err) => {
                console.log(err);
            })
        
        , 10000);
        
        return () => clearInterval(timer);
    });
    
    const doFindPeople = async () => {
        
        const response = await axios
        .get('http://localhost:5000/api/v1/scraper/google/findpeople', {params: {query}})
        .catch((err) => {
            console.log(err);
            
            return {
                status: 911,
                error: 'Unknown error',
                results: null,
            }
        });
        
        dispatch(findPeople(response.data));
    };
    
    const onChange = (event) => {
        setQuery(event.target.value);
    };
    
    return (
        <Menu stackable >
            <Menu.Item active name="people">
                People
            </Menu.Item>
            <Menu.Item name="cv">
                CV/Resume
            </Menu.Item>

            <Menu.Item name="search">
                <Input name="query" className="icon" icon="search" placeholder="Search..." value={query} onChange={onChange} />
            </Menu.Item>
            <Menu.Item name="submit">
                <Button onClick={doFindPeople}>Search</Button>
            </Menu.Item>
            {typeof people.status === 'string' && <Menu.Item name="status">
                {people.status.toUpperCase()}
            </Menu.Item>}
            <Menu.Item name="count">
                <Button as="div" labelPosition="right">
                    <Button icon>
                        <Icon name="linkedin" />
                    </Button>
                    <Label as="a" basic pointing="left">{people.linkedin.length}</Label>
                </Button>
                &nbsp;&nbsp;
                <Button as="div" labelPosition="right">
                    <Button icon>
                        <Icon name="twitter" />
                    </Button>
                    <Label as="a" basic pointing="left">{people.twitter.length}</Label>
                </Button>
                &nbsp;&nbsp;
                <Button as="div" labelPosition="left">
                    <Button icon>
                        <Icon name="facebook" />
                    </Button>
                    <Label as="a" basic pointing="left">{people.facebook.length}</Label>
                </Button>
            </Menu.Item>
        </Menu>
    );
};
    
export default Header;
    