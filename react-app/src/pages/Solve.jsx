import React, { useEffect, useState, useCallback } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import CodeMirror from "@uiw/react-codemirror";
import { vscodeDark } from "@uiw/codemirror-theme-vscode";
import { python } from '@codemirror/lang-python';
import MarkdownIt from 'markdown-it';
import Split from 'react-split';
import { Button } from '@mui/material';
import axios from 'axios';
import { HashLoader } from 'react-spinners';

function Solve() {
  const { problem } = useParams();
  const [markdownContent, setMarkdownContent] = useState('');
  const navigate = useNavigate();
  const [problemName, setProblemName] = useState('');
  const database_url = 'http://127.0.0.1:7432';
  const [value, setValue] = useState();

  const onChange = useCallback((val) => {
    setValue(val);
  }, []);

  useEffect(() => {
    async function fetchResult() {
      try {
        const post_data = { 'problem': problem };
        const response = await axios.post(database_url + '/get_problem_md_and_arguments', post_data);
        const markdown = response.data['markdown'];
        const args = response.data['arguments'];
        const joinedArgs = args.join(', ');

        setProblemName(`class Solution:\n  def ${problem}(self, ${joinedArgs}):\n  # Write your solution here\n\n`);
        const md = new MarkdownIt();
        const htmlContent = md.render(markdown);

        setMarkdownContent(htmlContent);
      } catch (error) {
        console.error(`Error while retrieving problems: ${error.message}`);
      }
    }

    fetchResult();
  }, [problem]);

  const redirectPage = () => {
    navigate('/result', { state: { problem: problem, user_code: value } });
  };

  const navigateHome = () => {
    navigate('/'); // Change this to the desired home route
  }

  return (
    <div>
      {markdownContent === '' ? (
        <div>
          <h1>Loading Problem</h1>
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '80px' }}>
            <HashLoader color="#36d7b7" size='100' />
          </div>
        </div>
      ) : (
        <div>
          <Button onClick={navigateHome}>Go Home</Button>
          <h1 className='h1'>The Clock has Started!</h1>
          <Split
            sizes={[50, 50]}
            minSize={100}
            expandToMin={false}
            gutterSize={50}
            direction='horizontal'
            mode='horizontal'
            className='solve-container'
          >
            <div
              dangerouslySetInnerHTML={{ __html: markdownContent }}
              style={{
                fontSize: '16px',
                lineHeight: '1.5',
                textAlign: 'left',
                width: '50vh',
              }}
              className="markdown-content"
            ></div>
            <div className='w-full overflow-auto'>
              <CodeMirror
                value={problemName}
                theme={vscodeDark}
                extensions={[python()]}
                style={{ textAlign: 'left' }}
                className="code-mirror-container"
                onChange={onChange}
              />
              <Button onClick={redirectPage}>Submit</Button>
            </div>
          </Split>
        </div>
      )}
    </div>
  );
}

export default Solve;