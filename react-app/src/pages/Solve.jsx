import React, { useEffect, useState, useCallback } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import CodeMirror from "@uiw/react-codemirror";
import { vscodeDark } from "@uiw/codemirror-theme-vscode";
// import { javascript } from "@codemirror/lang-javascript";
import { python } from '@codemirror/lang-python'
import MarkdownIt from 'markdown-it';
import Split from 'react-split';
import { Button } from '@mui/material';

function Solve() {
    // Get the current location
    // const location = useLocation();
  
    // Extract the 'problem' parameter from the URL
    const { problem } = useParams();
    const [markdownContent, setMarkdownContent] = useState('');
    const navigate = useNavigate()
    const [problemName, setProblemName] = useState('');

    const [value, setValue] = useState();
    const onChange = useCallback((val) => {
    //   console.log('val:', val);
      setValue(val);
    }, []);

    useEffect(() => {
        // Assuming problem.md is located in the public folder
        fetch(`/problems/${problem}.md`)
          .then((response) => response.text())
          .then((text) => {
            // Parse the Markdown content to HTML
            const md = new MarkdownIt();
            const htmlContent = md.render(text);
    
            setMarkdownContent(htmlContent);
          })
          .catch((error) => {
            console.error('Error loading Markdown content:', error);
          });
        
        setProblemName(`class Solution(object):\n  def ${problem}(self, nums, target):\n  # Write your solution here\n\n`)

    }, [problem]);

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
  


// function Solve() {
//   const { problem } = useParams();
//   const [markdownContent, setMarkdownContent] = useState('');

//   useEffect(() => {
//     // Assuming problem.md is located in the public folder
//     fetch(`/problem/${problem}.md`)
//       .then((response) => response.text())
//       .then((text) => {
//         // Parse the Markdown content to HTML
//         const md = new MarkdownIt();
//         const htmlContent = md.render(text);

//         setMarkdownContent(htmlContent);
//       })
//       .catch((error) => {
//         console.error('Error loading Markdown content:', error);
//       });
//   }, [problem]);

//   return (
//     <div dangerouslySetInnerHTML={{ __html: markdownContent }}></div>
//   );
// }

// export default Solve;


// return (
//     <Split
//       sizes={[25, 50, 25]} // Initial sizes of the panes in percentages
//       minSize={100} // Minimum size for a pane
//       expandToMin={false} // Whether to expand to the minimum size when resizing
//       gutterSize={10} // Size of the dividers (gutters)
//     >
//       <div>Pane 1</div>
//       <div>Pane 2</div>
//       <div>Pane 3</div>
//     </Split>
//   );
// }