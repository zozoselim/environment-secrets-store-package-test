# Environment Secrets Store Executor Implementation Report

## Purpose

Environment Secrets Store bileşeninin runtime çalışma mantığı geliştirilmiştir.

Bu executor, yapılandırmada verilen environment variable isimlerini çalışma
anında okuyarak secret değerleri workflow outputlarına dönüştürür.

## Configuration

Executor, PackageModel içerisinde tanımlanan aşağıdaki configuration değerini
kullanır:

```text
variables_storing_secrets: List[str]
```

Örnek:

```text
ACCESS_TOKEN
OPENAI_API_KEY
DATABASE_PASSWORD
```

## Runtime Behavior

Executor, listede bulunan her environment variable değerini Python `os`
modülü üzerinden okur.

Örnek dönüşüm:

```text
ACCESS_TOKEN → access_token
OPENAI_API_KEY → openai_api_key
DATABASE_PASSWORD → database_password
```

Environment variable isimleri küçük harfe dönüştürülerek dinamik output adı
olarak kullanılır.

## Error Handling

`variables_storing_secrets` listesi boşsa executor çalışmayı durdurur.

İstenen environment variable sistemde bulunamazsa aşağıdaki yapıda bir hata
oluşturulur:

```text
Required environment variable was not found: ACCESS_TOKEN
```

Hata mesajında yalnızca environment variable ismi gösterilir. Secret değeri
hata mesajına veya loglara eklenmez.

## Security

- Secret değerler kaynak kod içerisinde saklanmaz.
- Secret değerler loglanmaz.
- Secret değerler hata mesajlarında gösterilmez.
- Değerler yalnızca runtime sırasında okunur.
- `.env` dosyası GitHub ve Docker image dışında tutulur.
- Docker ortamında secret değerler `--env-file` veya `-e` kullanılarak
  container'a aktarılır.

## Response Structure

Her secret değeri için bir `SecretOutput` oluşturulur.

Oluşturulan dinamik outputlar `PackageOutputs` içerisine eklenir ve
NovaVision'ın beklediği response yapısı `PackageHelper` ile hazırlanır.

## Modified Files

```text
src/executors/EnvironmentSecretsStore.py
src/utils/response.py
```

Eski `Package.py` dosyası `EnvironmentSecretsStore.py` olarak yeniden
adlandırılmıştır.

## Verification

Python syntax kontrolü aşağıdaki komutla gerçekleştirilmiştir:

```powershell
python -m py_compile `
  .\src\executors\EnvironmentSecretsStore.py `
  .\src\utils\response.py `
  .\src\models\PackageModel.py
```

Komut hata vermeden tamamlanmıştır.

Environment variable aktarımı ayrıca Docker container içerisinde `.env`
dosyası kullanılarak test edilmiştir.

Runtime NovaVision entegrasyonu, Client App ve Clean Install Test görevlerinde
uçtan uca doğrulanacaktır.