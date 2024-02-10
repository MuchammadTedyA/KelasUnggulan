from django import forms
from .models import siswa


class dataSiswa(forms.ModelForm):
    class Meta:
        model = siswa
        fields = '__all__'
        # error_messages = {
        #     'nisn_siswa': {
        #         'required': 'Anda harus mengisi form NISN'
        #     },
        #     'nama_siswa': {
        #         'required': 'Anda harus mengisi form Nama Siswa'
        #     },
        #     'iq_siswa': {
        #         'required': 'Anda harus mengisi Tingkat IQ dengan angka'
        #     },
        #     'iq_huruf_siswa': {
        #         'required': 'Anda harus mengisi Tingkat IQ dengan huruf'
        #     },
        #     'rapor_ipa_siswa': {
        #         'required': 'Anda harus mengisi form rapor ipa siswa dengan angka'
        #     },
        #     'rapor_ips_siswa': {
        #         'required': 'Anda harus mengisi form rapor ips siswa dengan angka'
        #     },
        #     'rapor_bahasa_siswa': {
        #         'required': 'Anda harus mengisi form rapor bahasa siswa dengan angka'
        #     },
        #     'tpa_ipa_siswa': {
        #         'required': 'Anda harus mengisi form TPA ipa siswa dengan angka'
        #     },
        #     'tpa_ips_siswa': {
        #         'required': 'Anda harus mengisi form TPA ips siswa dengan angka'
        #     },
        #     'tpa_bahasa_siswa': {
        #         'required': 'Anda harus mengisi form TPA bahasa siswa dengan angka'
        #     }
        # }
