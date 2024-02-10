"""KelasUnggulan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from fahp.views import halamanUtama, inputSiswa, cekSiswa, ubahSiswa, updateSiswa, hapusSiswa, indexSiswa, indexKriteria, ubahKriteria, hapusKriteria,  subKriteria, hapusSubKriteria, ubahSubKriteria, pembobotanKriteria, bersihKriteria, fahpKriteria, pembobotanSubKriteria, bersihSubKriteria, subKriteriaPilih, fahpSubKriteria, indexHasil, simpanHasil, tampilLap, hapusLaporan, unduhLaporan
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', LoginView.as_view(), name=""),
    path('masuk/', LoginView.as_view(), name="masuk"),
    path('keluar/', LogoutView.as_view(next_page='masuk'), name="keluar"),

    path('beranda/', halamanUtama, name="beranda"),
    path('laporan/<str:id>', tampilLap, name="tampil_laporan"),
    path('hapusLaporan/<str:id>', hapusLaporan, name="hapus_laporan"),
    path('unduhLaporan/<str:id>', unduhLaporan, name="unduh_laporan"),


    path('siswa/', indexSiswa, name="siswa"),
    path('siswa/cek', cekSiswa, name="cekSiswa"),
    path('siswa/insert', inputSiswa, name="siswa_input"),
    path('siswa/ubah/<str:id>', ubahSiswa, name="siswa_ubah"),
    path('siswa/update', updateSiswa, name="siswa_update"),
    path('siswa/hapus/<str:id>', hapusSiswa, name="siswa_hapus"),

    path('kriteria', indexKriteria, name="kriteria"),
    path('kriteria/ubah/<str:id>', ubahKriteria, name="kriteria_ubah"),
    path('kriteria/hapus/<str:id>', hapusKriteria, name="kriteria_hapus"),
    path('kriteria/sub', subKriteria, name="subKriteria"),
    path('kriteria/sub/ubah/<str:id>', ubahSubKriteria, name="subKriteria_ubah"),
    path('kriteria/sub/hapus/<str:id>',
         hapusSubKriteria, name="subKriteria_hapus"),

    path('fahp/kriteria/', pembobotanKriteria, name="fahp"),
    path('fahp/kriteria/bersih', bersihKriteria, name="bersihFahp"),
    path('fahp/kriteria/fuzzy', fahpKriteria, name="fahp_kriteriaFuzzy"),

    path('fahp/subkriteria/', subKriteriaPilih, name="fahps"),
    path('fahp/subkriteria/bersih/<str:id_k>',
         bersihSubKriteria, name="bersihFahps"),
    path('fahp/subkriteria/<str:id_k>', pembobotanSubKriteria,
         name="pembobotanSubKriteria"),
    path('fahp/subkriteria/fuzzy/<str:id_k>',
         fahpSubKriteria, name="fahp_subKriteriaFuzzy"),

    path('fahp/hasil/', indexHasil, name="hasil"),
    path('fahp/hasil/simpan', simpanHasil, name="hasil_simpan"),

    path('admin', admin.site.urls),
]
