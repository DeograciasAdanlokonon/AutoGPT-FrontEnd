function UploadChatInterface() {
  const [messages, setMessages] = React.useState([]);
  const [inputMessage, setInputMessage] = React.useState('');
  const [isLoading, setIsLoading] = React.useState(false);
  const [uploadedFiles, setUploadedFiles] = React.useState([]);
  const fileInputRef = React.useRef(null);

  const handleFileUpload = (event) => {
    const files = Array.from(event.target.files);
    setUploadedFiles(prev => [...prev, ...files]);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const files = Array.from(event.dataTransfer.files);
    setUploadedFiles(prev => [...prev, ...files]);
  };

  const handleSendMessage = () => {
    if (!inputMessage.trim()) return;

    setMessages(prev => [...prev, {
      text: inputMessage,
      isUser: true,
      timestamp: new Date().toLocaleTimeString()
    }]);

    // Simuler une réponse de l'IA
    setIsLoading(true);
    setTimeout(() => {
      setMessages(prev => [...prev, {
        text: "Ceci est une simulation de réponse AutoGPT...",
        isUser: false,
        timestamp: new Date().toLocaleTimeString()
      }]);
      setIsLoading(false);
    }, 1000);

    setInputMessage('');
  };

  return React.createElement('div', {
    className: "h-screen w-full max-w-4xl mx-auto flex flex-col p-4 bg-gray-50"
  }, [
    // Zone de dépôt de fichiers
    React.createElement('div', {
      key: 'dropzone',
      className: "w-full p-8 mb-4 border-2 border-dashed border-blue-300 rounded-lg bg-white",
      onDragOver: handleDragOver,
      onDrop: handleDrop
    }, 
      React.createElement('div', {
        className: "text-center"
      }, [
        React.createElement(Upload, {
          key: 'upload-icon',
          className: "mx-auto h-12 w-12 text-gray-400 mb-4"
        }),
        React.createElement('p', {
          key: 'upload-text',
          className: "text-gray-600 mb-2"
        }, "Glissez vos fichiers ici ou"),
        React.createElement('button', {
          key: 'upload-button',
          onClick: () => fileInputRef.current?.click(),
          className: "bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        }, "Sélectionnez des fichiers"),
        React.createElement('input', {
          key: 'file-input',
          type: "file",
          multiple: true,
          className: "hidden",
          ref: fileInputRef,
          onChange: handleFileUpload
        })
      ])
    ),

    // Liste des fichiers téléchargés
    uploadedFiles.length > 0 && React.createElement('div', {
      key: 'uploaded-files',
      className: "mb-4 p-4 bg-white rounded-lg shadow"
    }, [
      React.createElement('h3', {
        key: 'files-title',
        className: "font-semibold mb-2"
      }, "Fichiers téléchargés:"),
      React.createElement('ul', {
        key: 'files-list',
        className: "space-y-2"
      }, uploadedFiles.map((file, index) => 
        React.createElement('li', {
          key: index,
          className: "text-sm text-gray-600"
        }, `${file.name} (${(file.size / 1024).toFixed(2)} KB)`)
      ))
    ]),

    // Zone de chat
    React.createElement('div', {
      key: 'chat-zone',
      className: "flex-1 bg-white rounded-lg shadow overflow-hidden flex flex-col"
    }, [
      React.createElement('div', {
        key: 'messages',
        className: "flex-1 p-4 overflow-y-auto space-y-4"
      }, [
        ...messages.map((message, index) => 
          React.createElement('div', {
            key: `message-${index}`,
            className: `flex ${message.isUser ? 'justify-end' : 'justify-start'}`
          }, 
            React.createElement('div', {
              className: `max-w-3/4 p-3 rounded-lg ${
                message.isUser
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-800'
              }`
            }, [
              React.createElement('p', {
                key: 'message-text'
              }, message.text),
              React.createElement('span', {
                key: 'message-timestamp',
                className: "text-xs opacity-75"
              }, message.timestamp)
            ])
          )
        ),
        isLoading && React.createElement('div', {
          key: 'loading',
          className: "flex justify-start"
        }, 
          React.createElement('div', {
            className: "bg-gray-100 p-3 rounded-lg"
          },
            React.createElement(Loader2, {
              className: "h-5 w-5 animate-spin text-blue-500"
            })
          )
        )
      ]),

      // Zone de saisie
      React.createElement('div', {
        key: 'input-zone',
        className: "p-4 border-t"
      },
        React.createElement('div', {
          className: "flex space-x-2"
        }, [
          React.createElement('input', {
            key: 'text-input',
            type: "text",
            value: inputMessage,
            onChange: (e) => setInputMessage(e.target.value),
            onKeyPress: (e) => e.key === 'Enter' && handleSendMessage(),
            placeholder: "Écrivez votre message...",
            className: "flex-1 p-2 border rounded-lg focus:outline-none focus:border-blue-500"
          }),
          React.createElement('button', {
            key: 'send-button',
            onClick: handleSendMessage,
            className: "bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600"
          },
            React.createElement(Send, {
              className: "h-5 w-5"
            })
          )
        ])
      )
    ])
  ]);
}

// Rendu du composant
ReactDOM.render(
  React.createElement(UploadChatInterface),
  document.getElementById('root')
);
