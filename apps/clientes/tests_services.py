from django.test import TestCase
from apps.clientes.models import Cliente, PersonaAutorizada
from apps.clientes.services import ClienteService
from core.exceptions import RecursoNoEncontradoError, ReglaDeNegocioError


class ClienteServiceTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombres="Luz", apellidos="Ramos",
            dni="44332211", correo="luz@test.com"
        )

    def test_obtener_o_error_existe(self):
        resultado = ClienteService.obtener_o_error(self.cliente.id)
        self.assertEqual(resultado, self.cliente)

    def test_obtener_o_error_no_existe(self):
        with self.assertRaises(RecursoNoEncontradoError):
            ClienteService.obtener_o_error(99999)

    def test_registrar_cliente_exitoso(self):
        nuevo = ClienteService.registrar_cliente({
            "nombres": "Mario", "apellidos": "Cruz", "dni": "55443322"
        })
        self.assertIsNotNone(nuevo.id)

    def test_registrar_cliente_correo_duplicado_falla(self):
        with self.assertRaises(ReglaDeNegocioError):
            ClienteService.registrar_cliente({
                "nombres": "Otro", "apellidos": "Cliente",
                "correo": "luz@test.com"
            })

    def test_agregar_persona_autorizada(self):
        persona = ClienteService.agregar_persona_autorizada(
            self.cliente.id,
            {"nombres": "Carlos Cruz", "dni": "11223344"}
        )
        self.assertEqual(persona.id_cliente, self.cliente)

    def test_agregar_persona_dni_duplicado_falla(self):
        ClienteService.agregar_persona_autorizada(
            self.cliente.id,
            {"nombres": "Carlos Cruz", "dni": "99887766"}
        )
        with self.assertRaises(ReglaDeNegocioError):
            ClienteService.agregar_persona_autorizada(
                self.cliente.id,
                {"nombres": "Pedro Paz", "dni": "99887766"}
            )

    def test_eliminar_persona_autorizada(self):
        persona = PersonaAutorizada.objects.create(
            id_cliente=self.cliente, nombres="Laura", dni="55667788"
        )
        ClienteService.eliminar_persona_autorizada(persona.id)
        self.assertFalse(PersonaAutorizada.objects.filter(pk=persona.id).exists())

    def test_eliminar_persona_no_existente_falla(self):
        with self.assertRaises(RecursoNoEncontradoError):
            ClienteService.eliminar_persona_autorizada(99999)
