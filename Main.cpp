//#include "stdafx.h"
#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>
#include <vector>
#include <cmath>
#include <locale>
#include <set>
#include "md5.h"
#include "md5.cpp"
using namespace std;

int main() {
    fstream db, names, q;
    db.open("/home/ruslan/PycharmProjects/Hash_test/test_data/smu_db.fasta");
    names.open("/home/ruslan/PycharmProjects/Hash_test/test_data/smu_ids.tsv");
    q.open("/home/ruslan/PycharmProjects/Hash_test/test_data/GCA_000829155.1.fasta");
    if ((db) && (names) && (q)) {
        cout << "YAS\n";
    }

    // ЧИТАЕМ ФАЙЛ NAMES
    string line, field;
    vector< vector<string> > array;  // the 2D array
    vector<string> v;                // array of values for one line only
    while (getline(names, line)) {
        v.clear();
        stringstream ss(line);
        while (getline(ss,field,'\t'))  // break line into comma delimitted fields
        {
            v.push_back(field);  // add each field to the 1D array
        }
        array.push_back(v);  // add the 1D array to the 2D array
    }

//    for (size_t i=0; i<array.size(); ++i)
//    {
//        for (size_t j=0; j<array[i].size(); ++j)
//        {
//            cout << array[i][j] << ' ';
//        }
//        cout << "\n";
//    }

    // Теперь у нас есть массив код - фигня



    vector< vector<string> > databa;

    // ПАРСИМ ФАСТУ ДБ
    string name, content;
    while (getline(db, line).good()) {
        v.clear();
        if (line.empty() || line[0] == '>') { // Identifier marker
            if (!name.empty()) { // Print out what we read from the last entry
//                cout << name << " : " << content << endl;
                size_t dot_pos = name.find(".");
                string cut_name = name.substr(0, dot_pos);
//                cout << cut_name << "\n";
                v.push_back(cut_name);
                v.push_back(content);
                databa.push_back(v);
                name.clear();
            }
            if (!line.empty()) {
                name = line.substr(1);
            }
            content.clear();
        } else if (!name.empty()) {
            if (line.find(' ') != string::npos) { // Invalid sequence--no spaces allowed
                name.clear();
                content.clear();
            } else {
                content += line;
            }
        }
    }
    if (!name.empty()) { // Print out what we read from the last entry
//        cout << name << " : " << content << endl;
        size_t dot_pos = name.find(".");
        string cut_name = name.substr(0, dot_pos);
        v.push_back(cut_name);
        v.push_back(content);
        databa.push_back(v);
    }
//    for (size_t i=0; i<databa.size(); ++i) {
//        for (size_t j=0; j<databa[i].size(); ++j)
//        {
//            cout << databa[i][j] << ' ';
//        }
//        cout << "\n";
//    }

    // Теперь у нас есть массив фигня - её последовательность


    // ХЕШИРУЕМ

    vector< vector<string> > dictionary;

    for (size_t i=0; i<databa.size(); ++i) {
        v.clear();
        string this_name = databa[i][0];
//            cout << this_name;
        string this_code = "NOT_FOUND";
        string this_seq = databa[i][1];
        string this_hash = md5(this_seq);

        int flag = 0;
        for (size_t p = 0; p < array.size(), flag == 0; ++p) {
            if (this_name == array[p][1]) {
                this_code = array[p][0];
                flag = 1;
            }
        }

        v.push_back(this_code);
        v.push_back(this_hash);
        dictionary.push_back(v);
    }

    for (size_t i=0; i<dictionary.size(); ++i) {
        for (size_t j=0; j<dictionary[i].size(); ++j) {
            cout << dictionary[i][j] << ' ';
        }
        cout << "\n";
    }

    // Получили словарь код - хэш

    set <string> st;

    // РАСЧЕХЛЯЕМ Q-ФАЙЛ, создаём сет хешей для запроса

    while (getline(q, line).good()) {
        v.clear();
        if (line.empty() || line[0] == '>') { // Identifier marker
            if (!name.empty()) { // Print out what we read from the last entry
//                cout << name << " : " << content << endl;
                size_t dot_pos = name.find(".");
                string cut_name = name.substr(0, dot_pos);
//                cout << cut_name << "\n";
                st.insert(md5(content));
                name.clear();
            }
            if (!line.empty()) {
                name = line.substr(1);
            }
            content.clear();
        } else if (!name.empty()) {
            if (line.find(' ') != string::npos) { // Invalid sequence--no spaces allowed
                name.clear();
                content.clear();
            } else {
                content += line;
            }
        }
    }
    if (!name.empty()) { // Print out what we read from the last entry
//        cout << name << " : " << content << endl;
        size_t dot_pos = name.find(".");
        string cut_name = name.substr(0, dot_pos);
        st.insert(md5(content));
    }

    set <string> st_found;
    int counter = 0;
    int total = 0;

    set <string> :: iterator it = st.begin();
    for (int i = 1; it != st.end(); i++, it++) {
        string this_hash = *it;
//        cout << this_hash << "\n";
        for (size_t p = 0; p < dictionary.size(); ++p) {
            if (this_hash == dictionary[p][1]) {
                st_found.insert(this_hash);
                counter++;
            }
        }
        total = i;
    }

    set <string> :: iterator it_found = st_found.begin();

    cout << counter << " of " << total << " found in the database\n";

    cout << "The present IPGs are:\n";

    for (int i = 1; it_found != st_found.end(); i++, it_found++) {
        cout << *it_found << "\n";
    }


    return 1;
}