# OneDrive Archive Uploader
> Realiza o upload de arquivos do seu computador para a nuvem do OneDrive, ele pode ser usado para fazer upload em massa de várias pastas e arquivos para múltiplas contas diferentes.  

[![NPM Version][npm-image]][npm-url]
[![Build Status][travis-image]][travis-url]

## Compilar o projeto
Primeiro faça um clone desse repositório em algum local no seu computador
```
git clone https://github.com/LucasPanao/UpOneDrive.git
```

Quando o clone estiver terminado, apenas execute o comando abaixo para instalar todas as dependências
```
npm install
```

## Exemplo de uso

Esse código foi feito para atender uma ou múltiplas contas do OneDrive tanto pessoais como empresariais, possibilitando o upload de arquivos em massa para várias contas diferetes, assim pode-se liberar espaço de sua máquina e administrar os arquivos através do serviço OneDrive da Microsoft. 

## Configuração para Desenvolvimento

Deve se ter instalado em sua máquina o python. Ao baixar/utilizar o projeto existem 2 arquivos .txt, esses serão os arquivos que o bot irá ler e executar as requisições. 

Dentro do arquivo list_drive.txt devem ser colocados todos os links relacionados ao drive das contas dos usuários que deseja subir os arquivos.

```sh
[URL_DRIVE_1]
[URL_DRIVE_2]
```

Dentro do arquivo list_folders.txt devem ser colocados os nomes das pastas que terão que subir dentro do diretório. Lembrando que deve estar alinhados a sequencia de usuários do list_drive.txt, pois cada pasta será designada a um usuário diferente(caso coloque outros usuários). 

```sh
[NOME_PASTA_1]
[NOME_PASTA_2]
```


## Histórico de lançamentos

* 1.0.0
    * O primeiro lançamento adequado

## Meta

Lucas Panão – [@LucasPanao](https://www.linkedin.com/in/lucas-panao/) – contato@panao.com.br

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

[https://github.com/LucasPanao]

## Contributing

1. Faça o _fork_ do projeto (<https://github.com/yourname/yourproject/fork>)
2. Crie uma _branch_ para sua modificação (`git checkout -b feature/fooBar`)
3. Faça o _commit_ (`git commit -am 'Add some fooBar'`)
4. _Push_ (`git push origin feature/fooBar`)
5. Crie um novo _Pull Request_

[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/seunome/seuprojeto/wiki


