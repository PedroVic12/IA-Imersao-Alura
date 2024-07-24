import 'package:flutter/material.dart';
import 'package:dio/dio.dart';

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final _textFieldController = TextEditingController();
  Map<String, dynamic>? dadosTreino;

  void _gerarTreino() async {
    String prompt = _textFieldController.text;

    try {
      var dio = Dio();
      var response =
          await dio.get('http://127.0.0.1:5000/treino?prompt=$prompt');

      if (response.statusCode == 200) {
        setState(() {
          dadosTreino = response.data;
        });
      } else {
        print('Erro na requisição: ${response.statusCode}');
      }
    } catch (e) {
      print('Erro: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Treino do Goku'),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: TextField(
                  controller: _textFieldController,
                  decoration: InputDecoration(
                    labelText: 'Digite seu prompt',
                  ),
                ),
              ),
              ElevatedButton(
                onPressed: _gerarTreino,
                child: Text('Gerar Treino'),
              ),
              SizedBox(height: 20),
              if (dadosTreino != null) Text(dadosTreino.toString()),
            ],
          ),
        ),
      ),
    );
  }
}
