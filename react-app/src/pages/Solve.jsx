import React, { useEffect, useState, useCallback } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import CodeMirror from "@uiw/react-codemirror";
import { vscodeDark } from "@uiw/codemirror-theme-vscode";
import { python } from '@codemirror/lang-python'
import MarkdownIt from 'markdown-it';
import Split from 'react-split';
import { Button } from '@mui/material';
import axios from 'axios';

function Solve() {
  
    // Extract the 'problem' parameter from the URL
    const { problem } = useParams();
    const [markdownContent, setMarkdownContent] = useState('');
    const navigate = useNavigate()
    const [problemName, setProblemName] = useState('');
    const database_url = 'http://127.0.0.1:7432'

    const [value, setValue] = useState();
    const onChange = useCallback((val) => {
    //   console.log('val:', val);
      setValue(val);
    }, []);

    useEffect(() => {

        async function fetchResult() {
          try {
            const post_data = {
              'problem': problem,
    
            };
            // post request with data
            const response = await axios.post(database_url + '/get_problem_md_and_arguments', post_data); // Replace with your API endpoint
            //console.log(response)
            const markdown = response.data['markdown'];
            const args = response.data['arguments'];
            const joinedArgs = args.join(', ');

            setProblemName(`class Solution(object):\n  def ${problem}(self, ${joinedArgs}):\n  # Write your solution here\n\n`)

            const md = new MarkdownIt();
            const htmlContent = md.render(markdown);
    
            setMarkdownContent(htmlContent); 
    
          } catch (error) {
            console.error(`Error while retrieving problems: ${error.message}`);
          }
        }
    
        fetchResult();
      }, []);
    

    const redirectPage = () => {
        navigate('/result', {state:{problem:problem, user_code:value}});
    }

    return (
        <div>
            <h1 className='h1'>The Clock has Started!</h1>
            <Split
                sizes={[50, 50]} // Initial sizes of the panes in percentages
                minSize={100} // Minimum size for a pane
                expandToMin={false} // Whether to expand to the minimum size when resizing
                gutterSize={50} // Size of the dividers (gutters)
                direction='horizontal'
                mode='horizontal'
                className='solve-container'
            >
                <div 
                    dangerouslySetInnerHTML={{ __html: markdownContent }}
                    style={{
                        /* Define your inline styles here */
                        fontSize: '16px',
                        lineHeight: '1.5',
                        textAlign: 'left',
                        width: '50vh',
                        /* Add more styles as needed */
                    }}
                    className="markdown-content"
                >
                </div>
                <div className='w-full overflow-auto'>
                    <CodeMirror
                        value={problemName}
                        theme={vscodeDark}
                        // onChange={onChange}
                        extensions={[python()]}
                        style={{textAlign: 'left'}}
                        className="code-mirror-container"
                        onChange={onChange}
                    />
                    <Button onClick={redirectPage}>Submit</Button>
                </div>
            </Split>
        </div>
    );
  }

  
  
  export default Solve;