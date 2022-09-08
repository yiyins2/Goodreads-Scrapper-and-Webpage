import './App.css';
// import './Collapsible.scss';

import React, { useState, useEffect } from 'react';
import Modal from 'react-modal';
import 'bootstrap/dist/css/bootstrap.css';
import BootstrapTable from 'react-bootstrap-table-next';
import 'react-bootstrap-table/css/react-bootstrap-table.css';
import paginationFactory from 'react-bootstrap-table2-paginator';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Collapsible from 'react-collapsible';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from "react-router-dom";

import BookSearchForm from './components/BookSearchForm'
import AuthorSearchForm from './components/AuthorSearchForm'
import BookAddForm from './components/BookAddForm'
import AuthorAddForm from './components/AuthorAddForm'
import BookEdit from './components/BookEdit'

import axios from 'axios';

function table() {
    const [books, setBooks] = useState([]);
    const [authors, setAuthors] = useState([]);

    function deleteBook(book_id) {
        axios.delete(`http://localhost:5000/book?id=${book_id}`)
            .then(
                (response) => {
                    setBooks(books.filter(book => book.book_id !== book_id));
                    toast.success("Successfully deleted book!")
                },
                (error) => {console.log(error);}
            );
    }

    function deleteAuthor(author_id) {
        axios.delete(`http://localhost:5000/author?id=${author_id}`)
            .then(
                (response) => {
                    setBooks(authors.filter(author => author.author_id !== author_id));
                    toast.success("Successfully deleted book!")
                },
                (error) => {console.log(error);}
            );
    }
    
    function bookEdit(book) {
        console.log(book)
        axios.put(`http://localhost:5000/author?id=${book.book_id}`, book)
            .then(
                (response) => {window.location.reload();},
                (error) => {toast.warn(error.response.data);}
            );
    }

    const book_columns = [{
            dataField: 'delete',
            formatter: (cell, row) => {
                return (
                    <div>
                    <button type="button" className="btn btn-outline-danger btn-block" onClick={() => {
                        var result = window.confirm("Want to delete?");
                        if (result) {
                            deleteBook(row.book_id)}
                        }
                    }>
                        Delete
                    </button>
                    {/* <BookEdit bookEdit={bookEdit} currentBook={row}/> */}
                    </div>
                );
            }
        }, {
            dataField: 'book_id',
            text: 'Book ID'
        }, {
            dataField: 'book_url',
            text: 'Title', 
            formatter: (cell, row) => {
                return <a href={cell}>{row.title}</a>; 
            }, 
            headerStyle: (colum, colIndex) => {
                return { width: '200px'};
            }
        }, {
            dataField: 'ISBN',
            text: 'ISBN'
        }, {
            dataField: 'author_url',
            text: 'Author', 
            formatter: (cell, row) => {
                return <a href={cell}>{row.author}</a>; 
            }, 
            headerStyle: (colum, colIndex) => {
                return { width: '100px'};
            }
        }, {
            dataField: 'image_url',
            text: 'Image', 
            formatter: imgFormatter
        }, {
            dataField: 'rating',
            text: 'Rating'
        }, {
            dataField: 'rating_count',
            text: 'Rating Count'
        }, {
            dataField: 'review_count',
            text: 'Review Count'
        }, {
            dataField: 'similar_books',
            text: 'Similar Books', 
            formatter: (cell, row) => {
                if (typeof row.similar_books !== 'undefined') {
                    return (
                        <Collapsible trigger="Click to see similar books">
                            {row.similar_books.map((value, index) => {
                                return <li><a href={value}>{row.similar_books_name[index]}</a></li>
                            })}
                        </Collapsible>
                    )
                }
            }
        }
    ];
    
    const author_columns = [{
            dataField: 'delete',
            formatter: (cell, row) => {
                return (
                    <div>
                    <button type="button" className="btn btn-outline-danger btn-block" onClick={() => {
                        var result = window.confirm("Want to delete?");
                        if (result) {
                            deleteAuthor(row.author_id)}
                        }
                    }>Delete</button>
                    <button type="button" className="btn btn-outline-info btn-block">
                        Edit
                    </button>
                    </div>
                );
            }
        }, {
            dataField: 'author_id',
            text: 'Author ID'
        }, {
            dataField: 'author_url',
            text: 'Name', 
            formatter: (cell, row) => {
                return <a href={cell}>{row.name}</a>; 
            }
        }, {
            dataField: 'image_url',
            text: 'Image', 
            formatter: imgFormatter
        }, {
            dataField: 'rating',
            text: 'Rating'
        }, {
            dataField: 'rating_count',
            text: 'Rating Count'
        }, {
            dataField: 'review_count',
            text: 'Review Count'
        }, {
            dataField: 'author_books',
            text: 'Author\'s Books', 
            formatter: (cell, row) => {
                if (typeof row.author_books !== 'undefined') {
                    return (
                        <Collapsible trigger="Click to see author's books">
                        {row.author_books.map((value, index) => {
                            return <li><a href={value}>{row.author_books_name[index]}</a></li>
                        })}
                        </Collapsible>
                    )
                }
            }, 
            headerStyle: (colum, colIndex) => {
                return { width: '250px'};
            }
        }, {
            dataField: 'similar_authors',
            text: 'Similar Authors', 
            formatter: (cell, row) => {
                if (typeof row.similar_authors !== 'undefined') {
                    return (
                        <Collapsible trigger="Click to see similar authors">
                        
                        {row.similar_authors.map((value, index) => {
                            return <li><a href={value}>{row.similar_authors_name[index]}</a></li>
                        })}
                        </Collapsible>
                    )
                }
            }, 
            headerStyle: (colum, colIndex) => {
                return { width: '250px'};
            }
        }
    ];
    
    function imgFormatter(cell, row) {
        return (
            <div className="text-center">
            <img src={cell} className="rounded mh-100" style={{width: "100px"}}></img>
            </div>
        ); 
    }

    function setBookSearch(bookField, bookQuery) {
        axios.get(`http://localhost:5000/search?q=book.${bookField}:${bookQuery}`)
            .then(
                (response) => {
                    setBooks([...response.data]);
                    toast.success("Successfully searched book!");
                },
                (error) => {
                    toast.warn(error.response.data); 
                }
            );
    }
    
    function setAuthorSearch(authorField, authorQuery) {
        axios.get(`http://localhost:5000/search?q=author.${authorField}:${authorQuery}`)
            .then(
                (response) => {
                    setAuthors([...response.data]);
                    toast.success("Successfully searched author!");
                },
                (error) => {
                    toast.warn(error.response.data); 
                }
            );
    }

    function bookAdd(book) {
        axios.post("http://localhost:5000/book", book) 
            .then(
                (response) => {
                    setBooks([...books, book]);
                    toast.success("Successfully added book!");
                },
                (error) => {
                    toast.warn(error.response.data); 
                }
            );
    }

    function authorAdd(author) {
        axios.post("http://localhost:5000/author", author) 
            .then(
                (response) => {
                    setAuthors([...authors, author]);
                    toast.success("Successfully added author!");
                },
                (error) => {
                    toast.warn(error.response.data); 
                }
            );
    }

    useEffect(() => {
        axios.get('http://localhost:5000/search?q=book.book_id:> 0')
            .then(
                (response) => {setBooks([...books, ...response.data]);},
                (error) => {console.log(error);}
            );
        axios.get('http://localhost:5000/search?q=author.author_id:> 0')
            .then(
                (response) => {setAuthors([...authors, ...response.data]);},
                (error) => {console.log(error);}
            );
    }, []);

    return (
        <div className="container">
        <p className="h1">Books</p>
        <div className="row">
        <BookSearchForm setBookSearch={setBookSearch}/>
        <BookAddForm bookAdd={bookAdd}/>
        </div>
        <BootstrapTable 
            keyField='book_id' 
            data={ books } 
            columns={ book_columns } 
            striped
            tabIndexCell
            wrapperClasses="table-responsive"
            pagination={ paginationFactory() }
        />
        <hr class="rounded"></hr>
        <p className="h1">Authors</p>
        <div className="row">
        <AuthorSearchForm setAuthorSearch={setAuthorSearch}/>
        <AuthorAddForm authorAdd={authorAdd}/>
        </div>
        <BootstrapTable 
            keyField='author_id' 
            data={ authors } 
            columns={ author_columns } 
            striped
            tabIndexCell
            wrapperClasses="table-responsive"
            pagination={ paginationFactory() }
        />
        <ToastContainer />
        </div>
    )
}

export default Table;